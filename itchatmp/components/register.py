import time, copy
import threading, logging
import traceback

import tornado
from tornado.web import RequestHandler
from tornado.wsgi import WSGIAdapter
from concurrent.futures import ThreadPoolExecutor

from itchatmp.content import (NORMAL, COMPATIBLE, SAFE,
    INCOME_MSG, OUTCOME_MSG, SERVER_WAIT_TIME)
from itchatmp.views import (
    deconstruct_msg, construct_xml_msg, reply_msg_format,
    decrypt_msg, encrypt_msg)
from itchatmp.controllers.oauth import oauth
from itchatmp.controllers.envtest import env_test
from itchatmp.exceptions import ParameterError
from itchatmp.log import set_logging

logger = logging.getLogger('itchatmp')

def load_register(core):
    core.update_config = update_config
    core.run = run
    core.msg_register = msg_register

def construct_get_post_fn(core):
    def get_fn(handler):
        if core.filterRequest and not core.filter_request(handler.request):
            return 'Greeting from itchatmp!'
        echostr = handler.get_argument('echostr', '')
        if handler.get_argument('msg_signature', ''):
            tns = [handler.get_argument(key, '') for
                key in ('timestamp', 'nonce', 'msg_signature')]
            valid = oauth(*(tns + [echostr, core.config.token]))
            echostr = decrypt_msg(*(tns + [core.config, {'echostr': echostr}]))
            echostr = echostr.get('echostr')
        else:
            valid = oauth(*([handler.get_argument(key, '') for
                key in ('timestamp', 'nonce', 'signature')]
                + [core.config.token]))
        return echostr if valid else 'Greeting from itchatmp!'
    def post_fn(handler):
        if core.filterRequest and not core.filter_request(handler.request):
            logger.debug('A request from unknown ip is filtered'); return None, None
        msgDict = deconstruct_msg(handler.request.body.decode('utf8', 'replace'))
        if handler.get_argument('msg_signature', ''):
            tns = [handler.get_argument(key, '') for
                key in ('timestamp', 'nonce', 'msg_signature')]
            valid = oauth(*(tns +
                [core.config.token, msgDict.get('Encrypt', '')]))
        else:
            tns = [handler.get_argument(key, '') for
                key in ('timestamp', 'nonce', 'signature')]
            valid = oauth(*(tns + [core.config.token]))
        if valid:
            isActualEncrypt = 'Encrypt' in msgDict
            if core.config.encryptMode == SAFE:
                msgDict = decrypt_msg(*(tns + [core.config, msgDict]))
            if not msgDict:
                logger.debug('Ignore a request because decrypt failed')
            else:
                try:
                    reply = get_reply_fn(core, msgDict['MsgType'])(copy.deepcopy(msgDict))
                except Exception as e:
                    logger.debug(traceback.format_exc())
                else:
                    reply = reply_msg_format(reply)
                    if reply:
                        if reply.get('MsgType') in OUTCOME_MSG:
                            reply['ToUserName'] = msgDict['FromUserName']
                            reply['FromUserName'] = msgDict['ToUserName']
                            if core.config.encryptMode == SAFE and isActualEncrypt:
                                return encrypt_msg(*(tns +
                                    [core.config, reply])), reply
                            else:
                                return construct_xml_msg(reply), reply
                        else:
                            logger.debug('Reply is invalid: unknown MsgType')
                    else:
                        logger.debug('Reply is invalid: %s' % reply.get('errmsg'))
        else:
            logger.debug('Ignore a request because of signature')
        return None, None
    return get_fn, post_fn

def construct_handler(core, isWsgi):
    get_fn, post_fn = construct_get_post_fn(core)
    if isWsgi:
        def _timer_thread(handler):
            time.sleep(SERVER_WAIT_TIME)
            if not closed: handler.finish()
        class MainHandler(RequestHandler):
            def get(core):
                core.finish(get_fn(core))
            def post(core):
                closed = False
                timeThread = threading.Thread(target=_timer_thread, args=(core,))
                timeThread.setDaemon = True
                timeThread.start()
                r, rawReply = post_fn(core)
                if closed:
                    if rawReply:
                        r = core.send(rawReply, rawReply.get('toUserName', ''))
                        if not r:
                            logger.debug('Reply error: %s' % r.get('errmsg', ''))
                else:
                    closed = True
                    core.finish(r)
    else:
        threadPool = ThreadPoolExecutor(core.threadPoolNumber)
        ioLoop = core.ioLoop
        class MainHandler(RequestHandler):
            def get(core):
                core.finish(get_fn(core))
            @tornado.gen.coroutine
            def post(core):
                timeoutHandler = ioLoop.call_later(SERVER_WAIT_TIME,
                    lambda: core.finish())
                r, rawReply = yield threadPool.submit(post_fn, core)
                ioLoop.remove_timeout(timeoutHandler)
                if time.time() < timeoutHandler.deadline:
                    core.finish(r)
                else:
                    if rawReply:
                        r = core.send(rawReply, rawReply.get('toUserName', ''))
                        if not r:
                            logger.debug('Reply error: %s' % r.get('errmsg', ''))
    return MainHandler

def update_config(self, config=None, atStorage=None, userStorage=None,
        filterRequest=None, threadPoolNumber=None):
    self.config = config or self.config
    self.atStorage = atStorage or self.atStorage
    self.userStorage = userStorage or self.userStorage
    self.filterRequest = filterRequest or self.filterRequest
    self.threadPoolNumber = threadPoolNumber or self.threadPoolNumber

def run(self, isWsgi=False, debug=True):
    self.isWsgi = isWsgi
    self.debug = debug
    set_logging(loggingLevel=logging.DEBUG if debug else logging.INFO)
    MainHandler = construct_handler(self, isWsgi)
    app = tornado.web.Application(
        [('/', MainHandler)], debug=debug)
    logger.info('itchatmp started!%s' % (
        ' press Ctrl+C to exit.' if debug else ''))
    if isWsgi:
        return WSGIAdapter(app)
    else:
        env_test()
        app.listen(80)
        try:
            self.ioLoop.start()
        except:
            logger.info('Bye~')
            self.ioLoop.stop()

def msg_register(self, msgType):
    ''' decorator to register message handlers
     * msgType can be type like TEXT or a list of them
     * register twice will override the older one
    '''
    def _msg_register(fn):
        msgTypeList = msgType if isinstance(msgType, list) else [msgType]
        for t in msgTypeList:
            if t in INCOME_MSG:
                self._replyFnDict[t] = fn
            else:
                raise ParameterError(
                    'Known type register "%s"' % t)
        return fn
    return _msg_register

def get_reply_fn(core, msgType):
    return core._replyFnDict.get(msgType, lambda x: None)
