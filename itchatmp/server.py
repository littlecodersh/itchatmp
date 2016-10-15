import functools, time, os
from base64 import b64decode

import tornado
from tornado.web import RequestHandler
from tornado.wsgi import WSGIAdapter
from concurrent.futures import ThreadPoolExecutor

from .content import (NORMAL, COMPATIBLE, SAFE,
    INCOME_MSG, OUTCOME_MSG,
    SERVER_WAIT_TIME)
from .views import construct_msg, deconstruct_msg
from .controllers.oauth import oauth, decrypt_msg, encrypt_msg
from .exceptions import ParameterError

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
            raise ParameterError('Wrong AES Key format')
    def verify(self):
        return True

class WechatServer(object):
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
            if self.filterRequest and not self._filter_request(handler): return ''
            echostr = handler.get_argument('echostr', '')
            if handler.get_argument('msg_signature', ''):
                tns = [handler.get_argument(key, '') for
                    key in ('timestamp', 'nonce', 'msg_signature')]
                valid = oauth(*(tns + [echostr, self.config.token]))
                echostr = decrypt_msg(*(tns + [self.config, {'echostr': echostr}]))
                echostr = echostr['echostr']
            else:
                valid = oauth(*([handler.get_argument(key, '') for
                    key in ('timestamp', 'nonce', 'signature')]
                    + [self.config.token]))
            if valid: return echostr
        def post_fn(handler):
            if self.filterRequest and not self._filter_request(handler):
                return ''
            tns = [handler.get_argument(key, '') for
                key in ('timestamp', 'nonce', 'signature')]
            valid = oauth(*(tns + [self.config.token]))
            if valid:
                msgDict = deconstruct_msg(
                    handler.request.body.decode('utf8', 'replace'))
                isActualEncrypt = 'Encrypt' in msgDict
                if self.config.encryptMode == SAFE:
                    msgDict = decrypt_msg(*(tns + [self.config, msgDict]))
                if not msgDict:
                    return ''
                else:
                    replyDict = self.__get_reply_fn(msgDict['MsgType'])(msgDict)
                if replyDict is None:
                    return ''
                elif replyDict.get('MsgType') in OUTCOME_MSG:
                    if self.config.encryptMode == SAFE and isActualEncrypt:
                        return encrypt_msg(*(tns + [self.config, msgDict, replyDict]))
                    else:
                        return construct_msg(msgDict, replyDict)
                else:
                    raise ParameterError(
                        'Unknown reply message type "%s"' % replyDict.get('MsgType'))
        return get_fn, post_fn
    def __construct_handler(self, isWsgi):
        get_fn, post_fn = self.__construct_get_post_fn()
        if isWsgi:
            class MainHandler(RequestHandler):
                def get(self):
                    self.finish(get_fn(self))
                def post(self):
                    self.finish(post_fn(self))
        else:
            threadPool = ThreadPoolExecutor(self.threadPoolNumber)
            ioLoop = self.ioLoop
            class MainHandler(RequestHandler):
                def get(self):
                    self.finish(get_fn(self))
                @tornado.gen.coroutine
                def post(self):
                    # WeChat server will close the connection in 5s
                    timeoutHandler = ioLoop.call_later(SERVER_WAIT_TIME,
                        lambda x: self.finish())
                    r = yield threadPool.submit(post_fn, self)
                    ioLoop.remove_timeout(timeoutHandler)
                    if time.time() < timeoutHandler.deadline:
                        self.finish(r)
                    else:
                        pass
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
        def _msg_register(fn):
            if msgType in INCOME_MSG:
                self.__replyFnDict[msgType] = fn
            else:
                raise ParameterError(
                    'Known type register "%s"' % msgType)
            return fn
        return _msg_register
    def __get_reply_fn(self, msgType):
        return self.__replyFnDict.get(msgType, lambda x: None)
