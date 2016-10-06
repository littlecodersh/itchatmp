import tornado
from tornado.web import RequestHandler
from concurrent.futures import ThreadPoolExecutor

from .content import (NORMAL, COMPATIBLE, SAFE,
    TEXT, IMAGE, VOICE, VIDEO, MUSIC, NEWS, TRANSFER)
from .controllers.oauth import oauth
from .views import construct_msg, deconstruct_msg
from .exceptions import ItChatSDKException

class WechatConfig(object):
    def __init__(self, token='', appId='', appSecret='',
            encryptMode=NORMAL, encodingAesKey=''):
        self.token = token
        self.appId, self.appSecret = appId, appSecret
        self.encryptMode = encryptMode
        self.encodingAesKey = encodingAesKey
    def verify(self):
        return True

class WechatServer(object):
    __replyFnDict = {}
    def __init__(self, config, atStorage, userStorage, threadPoolNumber=None):
        self.config = config
        self.atStorage = atStorage
        self.userStorage = userStorage
        self.threadPoolNumber = threadPoolNumber
    def __construct_get_post_fn(self):
        def get_fn(handler):
            valid = oauth(*([handler.get_argument(key, '') for
                key in ('timestamp', 'nonce', 'signature')]
                + [self.config.token]))
            if valid: return handler.get_argument('echostr', '')
        def post_fn(handler):
            valid = oauth(*([handler.get_argument(key, '') for
                key in ('timestamp', 'nonce', 'signature')]
                + [self.config.token]))
            if 1: # valid:
                msgDict = deconstruct_msg(
                    handler.request.body.decode('utf8', 'replace'))
                replyDict = self.__get_reply_fn(msgDict['MsgType'])(msgDict)
                if replyType is not None:
                    return construct_msg(msgDict, replyDict)
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
            class MainHandler(RequestHandler):
                def get(self):
                    self.finish(get_fn(self))
                @tornado.gen.coroutine
                def post(self):
                    r = yield threadPool.submit(post_fn, self)
                    self.finish(r)
        return MainHandler
    def update_config(self, config=None, atStorage=None, userStorage=None,
            threadPoolNumber=None):
        self.config = config or self.config
        self.atStorage = atStorage or self.atStorage
        self.userStorage = userStorage or self.userStorage
        self.threadPoolNumber = threadPoolNumber or self.threadPoolNumber
    def run(self, isWsgi=False, debug=True):
        MainHandler = self.__construct_handler(isWsgi)
        app = tornado.web.Application(
            [('/', MainHandler)], debug=debug)
        if isWsgi:
            return tornado.wsgi.WSGIAdapter(app)
        else:
            app.listen(80)
            tornado.ioloop.IOLoop.current().start()
    def msg_register(self, msgType):
        def _msg_register(fn):
            if msgType in (TEXT, TEXT, IMAGE,
                    VOICE, VIDEO, MUSIC, NEWS, TRANSFER)
                self.__replyFnDict[msgType] = fn
            else:
                raise ItChatSDKException(
                    'Known type register "%s"' % msgType)
            return fn
        return _msg_register
    def __get_reply_fn(self, msgType):
        return self.__replyFnDict.get(msgType, lambda x: (None, None))
