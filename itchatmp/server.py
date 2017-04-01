import os, logging
from base64 import b64decode

import tornado

from .content import NORMAL
from .controllers import (
    Application, Chat, Common, CustomerService,
    Menu, Messages, Oauth2, Statistics,
    TemplateMsgs, Users, Utils, Wrapped)
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
    ''' Wechat server class '''
    def __init__(self, config, atStorage, userStorage,
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
        # init apis
        self.application = Application(self)
        self.chat = Chat(self)
        self.common = Common(self)
        self.customerservice = CustomerService(self)
        self.menu = Menu(self)
        self.messages = Messages(self)
        self.oauth2 = Oauth2(self)
        self.statistics = Statistics(self)
        self.templatemsgs = TemplateMsgs(self)
        self.users = Users(self)
        self.utils = Utils(self)
        self.wrapped = Wrapped(self)
    def update_config(self, config=None, atStorage=None, userStorage=None,
            filterRequest=None, threadPoolNumber=None):
        ''' it is defined in components/register '''
        raise NotImplementedError()
    def run(self, isWsgi=False, debug=True, port=80):
        ''' it is defined in components/register '''
        raise NotImplementedError()
    def msg_register(self, msgType):
        ''' it is defined in components/register '''
        raise NotImplementedError()
    def upload(self, fileType, fileDir, additionalDict={}, permanent=False):
        return self.messages.upload(fileType, fileDir, additionalDict, permanent)
    def send(self, msg, toUserName, mediaId=None):
        return self.wrapped.send(msg, toUserName, mediaId)
    def filter_request(self, request):
        ''' this is not open for calling '''
        return self.common.filter_request(request)
    def access_token(self, fn):
        return self.common.access_token(fn)
    def clear_quota(self):
        return self.common.clear_quota()

load_register(WechatServer)
