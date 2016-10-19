import functools, time, os
import threading, logging
import traceback
from base64 import b64decode

import tornado
from tornado.web import RequestHandler
from tornado.wsgi import WSGIAdapter
from concurrent.futures import ThreadPoolExecutor

from .content import (NORMAL, COMPATIBLE, SAFE,
    INCOME_MSG, OUTCOME_MSG,
    SERVER_WAIT_TIME)
from .views import deconstruct_msg, construct_xml_msg, reply_msg_format
from .controllers.oauth import oauth, decrypt_msg, encrypt_msg
from .exceptions import ParameterError

logger = logging.getLogger('itchatmp')

class WechatConfig(object):
    ''' config storing class
     * if copId is set, appId will be ignored
    '''
    def __init__(self, token='', copId='', appId='', appSecret='',
            encryptMode=NORMAL, encodingAesKey=''):
        self.token = token
        self.copId, self.appId, self.appSecret = copId, appId, appSecret
        self.encryptMode = encryptMode
        self.encodingAesKey = encodingAesKey
        try:
            self._encodingAesKey = b64decode(
                self.encodingAesKey.encode('utf8') + b'=')
        except:
            if self.encryptMode == SAFE:
                raise ParameterError('Wrong AES Key format')
            else:
                self._encodingAesKey = ''
    def verify(self):
        return True

class WechatServer(object):
    ''' Wechat server class
     * _cssend and _filter_request will be automatically added when model loaded
     * is a singleton
    '''
    __replyFnDict = {}
    def __init__(self, config, atStorage, userStorage,
            filterRequest=False, threadPoolNumber=None):
        self.config = config
        self.atStorage = atStorage
        self.userStorage = userStorage
        self.filterRequest = filterRequest
        self.threadPoolNumber = threadPoolNumber or ((None
            if not hasattr(os, 'cpu_count') else os.cpu_count()) or 1) * 5
        try:
            self.ioLoop = tornado.ioloop.IOLoop.current()
        except:
            self.ioLoop = None
        self.isWsgi = True
        self.debug = True
    @staticmethod
    def instance():
        ''' singleton
         * initial a fake server only for storing necessary info
         * real server will be created in run
        '''
        if not hasattr(WechatServer, '_instance'):
            WechatServer._instance = WechatServer(WechatConfig(), None, None)
        return WechatServer._instance
    def _filter_request(self, request):
        '''
        will be defined in controllers.mpapi.common
        '''
        raise NotImplementedError()
    def __construct_get_post_fn(self):
        def get_fn(handler):
            if self.filterRequest and not self._filter_request(handler.request): return ''
            print(handler.get_argument('code', 'code'))
            print(handler.get_argument('state', 'state'))
            echostr = handler.get_argument('echostr', '')
            if handler.get_argument('msg_signature', ''):
                tns = [handler.get_argument(key, '') for
                    key in ('timestamp', 'nonce', 'msg_signature')]
                valid = oauth(*(tns + [echostr, self.config.token]))
                echostr = decrypt_msg(*(tns + [self.config, {'echostr': echostr}]))
                echostr = echostr.get('echostr')
            else:
                valid = oauth(*([handler.get_argument(key, '') for
                    key in ('timestamp', 'nonce', 'signature')]
                    + [self.config.token]))
            if valid: return echostr
        def post_fn(handler):
            if self.filterRequest and not self._filter_request(handler.request):
                logger.debug('A request from unknown ip is filtered'); return None, None
            msgDict = deconstruct_msg(handler.request.body.decode('utf8', 'replace'))
            if handler.get_argument('msg_signature', ''):
                tns = [handler.get_argument(key, '') for
                    key in ('timestamp', 'nonce', 'msg_signature')]
                valid = oauth(*(tns +
                    [self.config.token, msgDict.get('Encrypt', '')]))
            else:
                tns = [handler.get_argument(key, '') for
                    key in ('timestamp', 'nonce', 'signature')]
                valid = oauth(*(tns + [self.config.token]))
            if valid:
                isActualEncrypt = 'Encrypt' in msgDict
                if self.config.encryptMode == SAFE:
                    msgDict = decrypt_msg(*(tns + [self.config, msgDict]))
                if not msgDict:
                    logger.debug('Ignore a request because decrypt failed')
                else:
                    newMsgDict = {}
                    for k, v in msgDict.items(): newMsgDict[k[0].lower() + k[1:]] = v
                    try:
                        reply = self.__get_reply_fn(msgDict['MsgType'])(newMsgDict)
                    except Exception as e:
                        logger.debug(e.message)
                        if self.debug: traceback.print_exc()
                    else:
                        reply = reply_msg_format(reply)
                        if reply:
                            if reply.get('msgType') in OUTCOME_MSG:
                                reply['toUserName'] = msgDict['FromUserName']
                                reply['fromUserName'] = msgDict['ToUserName']
                                if self.config.encryptMode == SAFE and isActualEncrypt:
                                    return encrypt_msg(*(tns +
                                        [self.config, reply])), reply
                                else:
                                    return construct_xml_msg(reply), reply
                            else:
                                logger.debug('Reply is invalid: unknown msgType')
                        else:
                            logger.debug('Reply is invalid: %s' % reply.get('errmsg'))
            else:
                logger.debug('Ignore a request because of signature')
            return None, None
        return get_fn, post_fn
    def __construct_handler(self, isWsgi):
        get_fn, post_fn = self.__construct_get_post_fn()
        cssend = self._cssend
        if isWsgi:
            def _timer_thread(handler):
                time.sleep(SERVER_WAIT_TIME)
                if not closed: handler.finish()
            class MainHandler(RequestHandler):
                def get(self):
                    self.finish(get_fn(self))
                def post(self):
                    closed = False
                    timeThread = threading.Thread(target=_timer_thread, args=(self,))
                    timeThread.setDaemon = True
                    timeThread.start()
                    r, rawReply = post_fn(self)
                    if closed:
                        if rawReply:
                            r = cssend(rawReply, rawReply.get('toUserName', ''))
                            if not r:
                                logger.debug('Reply error: %s' % r.get('errmsg', ''))
                    else:
                        closed = True
                        self.finish(r)
        else:
            threadPool = ThreadPoolExecutor(self.threadPoolNumber)
            ioLoop = self.ioLoop
            class MainHandler(RequestHandler):
                def get(self):
                    self.finish(get_fn(self))
                @tornado.gen.coroutine
                def post(self):
                    timeoutHandler = ioLoop.call_later(SERVER_WAIT_TIME,
                        lambda: self.finish())
                    r, rawReply = yield threadPool.submit(post_fn, self)
                    ioLoop.remove_timeout(timeoutHandler)
                    if time.time() < timeoutHandler.deadline:
                        self.finish(r)
                    else:
                        if rawReply:
                            r = cssend(rawReply, rawReply.get('toUserName', ''))
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
        MainHandler = self.__construct_handler(isWsgi)
        app = tornado.web.Application(
            [('/', MainHandler)], debug=debug)
        if isWsgi:
            return WSGIAdapter(app)
        else:
            app.listen(80)
            try:
                self.ioLoop.start()
            except:
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
                    self.__replyFnDict[t] = fn
                else:
                    raise ParameterError(
                        'Known type register "%s"' % t)
            return fn
        return _msg_register
    def __get_reply_fn(self, msgType):
        return self.__replyFnDict.get(msgType, lambda x: None)
