import os, logging
from base64 import b64decode

import tornado

from .content import NORMAL
from .components import load_register
from .exceptions import ParameterError
from .models.common import TestStorage

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
    '''
        Wechat server class
    '''
    def __new__(cls, config, atStorage, userStorage,
            filterRequest=False, threadPoolNumber=None):
        ''' 
            this is a singleton
        '''
        if not hasattr(cls, '_instance'):
            cls._instance = super(WechatServer, cls).__new__(cls)
            cls._instance.init(config, atStorage, userStorage,
                filterRequest, threadPoolNumber)
            load_register(cls)
        return cls._instance
    def init(self, config, atStorage, userStorage,
            filterRequest=False, threadPoolNumber=None):
        # init configurations
        self.config = config
        self.atStorage = atStorage or TestStorage()
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
        self._replyFnDict = {}
    def update_config(self, config=None, atStorage=None, userStorage=None,
            filterRequest=None, threadPoolNumber=None):
        '''
            it is defined in components/register
        '''
        raise NotImplementedError()
    def run(self, isWsgi=False, debug=True, port=80):
        '''
            it is defined in components/register
        '''
        raise NotImplementedError()
    def msg_register(self, msgType):
        '''
            it is defined in components/register
        '''
        raise NotImplementedError()
    def upload(fileType, fileDir, additionalDict={}, permanent=False):
        '''
            it is defined in controllers/messages.py
        '''
        raise NotImplementedError()
    def send(self, msg, toUserName, mediaId=None):
        '''
            it is defined in controllers/wrapped.py
        '''
        raise NotImplementedError()
    def filter_request(self, request):
        '''
            this is not open for calling
            it is defined in controllers/common.py
        '''
        raise NotImplementedError()
    def access_token(self, fn):
        '''
            it is defined in controllers/common.py
        '''
        raise NotImplementedError()
    def clear_quota(self):
        '''
            it is defined in controllers/common.py
        '''
        raise NotImplementedError()
