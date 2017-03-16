import time, copy
import threading, logging
import traceback

import tornado
from tornado import gen
from tornado.web import RequestHandler
from tornado.wsgi import WSGIAdapter
from concurrent.futures import ThreadPoolExecutor

from itchatmp.config import SERVER_WAIT_TIME, COROUTINE
from itchatmp.content import (NORMAL, COMPATIBLE, SAFE,
    TEXT, INCOME_MSG, OUTCOME_MSG)
from itchatmp.views import (
    deconstruct_msg, construct_msg, reply_msg_format,
    decrypt_msg, encrypt_msg, oauth)
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
        ''' only for verifying server
            return echostr if verify
            return greeting words if not
        '''
        if core.filterRequest and not core.filter_request(handler.request):
            logger.debug('A request from unknown ip is filtered')
            return 'Greeting from itchatmp!'
        else:
            return verify_echostr(core, handler) or 'Greeting from itchatmp!'
    def sync_post_fn(handler):
        if core.filterRequest and not core.filter_request(handler.request):
            logger.debug('A request from unknown ip is filtered')
            return None, None
        else:
            msgDict = deconstruct_msg(handler.request.body)
            isActualEncrypt = 'Encrypt' in msgDict
            tns = get_tns(core, handler)
            msgDict = verify_message(core, handler, tns, msgDict)
            if not msgDict:
                logger.debug('Ignore a request because verify failed')
            else:
                reply_fn = get_reply_fn(core, msgDict['MsgType'])
                if reply_fn is None:
                    return None, None
                try:
                    reply = reply_fn(copy.deepcopy(msgDict))
                except Exception as e:
                    logger.warning(traceback.format_exc())
                else: # if nothing goes wrong
                    if reply:
                        return verify_reply(core, tns, reply, msgDict, isActualEncrypt)
        return None, None
    @gen.coroutine
    def coroutine_post_fn(handler):
        if core.filterRequest and not core.filter_request(handler.request):
            logger.debug('A request from unknown ip is filtered')
        else:
            msgDict = deconstruct_msg(handler.request.body)
            tns = get_tns(core, handler)
            isActualEncrypt = 'Encrypt' in msgDict
            msgDict = verify_message(core, handler, tns, msgDict)
            if not msgDict:
                logger.debug('Ignore a request because verify failed')
            else:
                reply_fn = get_reply_fn(core, msgDict['MsgType'])
                if reply_fn is None:
                    raise gen.Return((None, None))
                try:
                    reply = yield reply_fn(copy.deepcopy(msgDict))
                except Exception as e:
                    logger.warning(traceback.format_exc())
                else: # if nothing goes wrong
                    if reply:
                        r = yield verify_reply(core, tns, reply, msgDict, isActualEncrypt)
                        raise gen.Return(r)
        raise gen.Return((None, None))
    return get_fn, coroutine_post_fn if COROUTINE else sync_post_fn

def get_tns(core, handler):
    if handler.get_argument('msg_signature', ''):
        tns = [handler.get_argument(key, '') for
            key in ('timestamp', 'nonce', 'msg_signature')]
    else:
        tns = [handler.get_argument(key, '') for
            key in ('timestamp', 'nonce', 'signature')]
    return tns

def verify_echostr(core, handler):
    '''
        verify signature and return echostr if valid
        if not, None will be returned
    '''
    tns = get_tns(core, handler)
    echostr = handler.get_argument('echostr', '')
    if handler.get_argument('msg_signature', ''):
        if oauth(*(tns + [echostr, core.config.token])):
            msgDict = decrypt_msg(*(tns + [core.config, {'echostr': echostr}]))
            echostr = msgDict.get('echostr')
    else:
        valid = oauth(*(tns + [core.config.token]))
        if not valid:
            echostr = None
    return echostr

def verify_message(core, handler, tns, msgDict):
    '''
        verify signature and return decrypted message if valid
        if not, None will be returned
    '''
    if handler.get_argument('msg_signature', ''):
        valid = oauth(*(tns +
            [core.config.token, msgDict.get('Encrypt', '')]))
    else:
        valid = oauth(*(tns + [core.config.token]))
    if valid:
        if core.config.encryptMode == SAFE:
            msgDict = decrypt_msg(*(tns + [core.config, msgDict]))
    else:
        msgDict = {}
    return msgDict

if COROUTINE:
    @gen.coroutine
    def verify_reply(core, tns, reply, msgDict, isActualEncrypt):
        reply = reply_msg_format(reply)
        if reply:
            if reply.get('MsgType') in OUTCOME_MSG:
                reply['ToUserName'] = msgDict['FromUserName']
                reply['FromUserName'] = msgDict['ToUserName']
                if 'FileDir' in reply and reply['MsgType'] != TEXT:
                    r = yield core.upload(reply['MsgType'], reply['FileDir'])
                    if not r:
                        logger.warning(r)
                        raise gen.Return((None, None))
                    else:
                        reply['MediaId'] = r['media_id']
                if core.config.encryptMode == SAFE and isActualEncrypt:
                    raise gen.Return((encrypt_msg(*(tns +
                        [core.config, reply])), reply))
                else:
                    raise gen.Return((construct_msg(reply), reply))
            else:
                logger.warning('Reply is invalid: unknown MsgType')
        else:
            logger.warning('Reply is invalid: %s' % reply.get('errmsg'))
        raise gen.Return((None, None))
else:
    def verify_reply(core, tns, reply, msgDict, isActualEncrypt):
        reply = reply_msg_format(reply)
        if reply:
            if reply.get('MsgType') in OUTCOME_MSG:
                reply['ToUserName'] = msgDict['FromUserName']
                reply['FromUserName'] = msgDict['ToUserName']
                if 'FileDir' in reply and reply['MsgType'] != TEXT:
                    r = core.upload(reply['MsgType'], reply['FileDir'])
                    if not r:
                        logger.warning(r); return None, None
                    else:
                        reply['MediaId'] = r['media_id']
                if core.config.encryptMode == SAFE and isActualEncrypt:
                    return encrypt_msg(*(tns +
                        [core.config, reply])), reply
                else:
                    return construct_msg(reply), reply
            else:
                logger.warning('Reply is invalid: unknown MsgType')
        else:
            logger.warning('Reply is invalid: %s' % reply.get('errmsg'))
        return None, None

def construct_handler(core, isWsgi):
    get_fn, post_fn = construct_get_post_fn(core)
    class BaseHandler(RequestHandler):
        def initialize(self):
            self.closed = False
        def on_connection_close(self):
            self.closed = True
        def get(self):
            self.finish(get_fn(self))
    if isWsgi:
        class MainHandler(BaseHandler):
            def post(self):
                r, rawReply = post_fn(self)
                if self.closed: # server has stopped waiting
                    if rawReply:
                        r = core.send(rawReply, rawReply.get('ToUserName', ''))
                        if not r:
                            logger.warning('Reply error: %s' % r.get('errmsg', ''))
                else:
                    self.finish(r)
    else:
        ioLoop = core.ioLoop
        if COROUTINE:
            class MainHandler(BaseHandler):
                @tornado.gen.coroutine
                def post(self):
                    def time_out_callback():
                        self.finish()
                        self.closed = True
                    timeoutHandler = ioLoop.call_later(SERVER_WAIT_TIME,
                        time_out_callback)
                    r, rawReply = yield post_fn(self)
                    ioLoop.remove_timeout(timeoutHandler)
                    if self.closed:
                        if rawReply:
                            r = yield core.send(rawReply, rawReply.get('ToUserName', ''))
                            if not r:
                                logger.warning('Reply error: %s' % r.get('errmsg', ''))
                    else:
                        self.finish(r)
        else:
            threadPool = ThreadPoolExecutor(core.threadPoolNumber)
            class MainHandler(BaseHandler):
                @tornado.gen.coroutine
                def post(self):
                    def time_out_callback():
                        self.finish()
                        self.closed = True
                    timeoutHandler = ioLoop.call_later(SERVER_WAIT_TIME,
                        time_out_callback)
                    r, rawReply = yield threadPool.submit(post_fn, self)
                    ioLoop.remove_timeout(timeoutHandler)
                    if self.closed:
                        if rawReply:
                            r = yield threadPool.submit(core.send,
                                (rawReply, rawReply.get('ToUserName', '')))
                            if not r:
                                logger.warning('Reply error: %s' % r.get('errmsg', ''))
                    else:
                        self.finish(r)
    return MainHandler

def update_config(self, config=None, atStorage=None, userStorage=None,
        filterRequest=None, threadPoolNumber=None):
    self.config = config or self.config
    self.atStorage = atStorage or self.atStorage
    self.userStorage = userStorage or self.userStorage
    self.filterRequest = filterRequest or self.filterRequest
    self.threadPoolNumber = threadPoolNumber or self.threadPoolNumber

def run(self, isWsgi=False, debug=True, port=80):
    self.isWsgi = isWsgi
    self.debug = debug
    if debug:
        set_logging(loggingLevel=logging.DEBUG)
    MainHandler = construct_handler(self, isWsgi)
    app = tornado.web.Application(
        [('/', MainHandler)], debug=debug)
    logger.info('itchatmp started!%s' % (
        ' press Ctrl+C to exit.' if debug else ''))
    if isWsgi:
        return WSGIAdapter(app)
    else:
        port = int(port)
        env_test(port)
        app.listen(port)
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
        if COROUTINE:
            fn = gen.coroutine(fn)
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
    return core._replyFnDict.get(msgType)
