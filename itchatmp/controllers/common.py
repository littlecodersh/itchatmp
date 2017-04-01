from tornado.concurrent import Future

from itchatmp.utils import CoreMixin
from .mpapi.mp import common as mpCommon
from .mpapi.qy import common as qyCommon

class BaseController(CoreMixin):
    def determine_wrapper(self, mpFn=None, copFn=None, *args, **kwargs):
        tokenFn = self.core.common.access_token
        if 'needToken' in kwargs:
            if not kwargs['needToken']:
                tokenFn = lambda fn: fn
            del kwargs['needToken']
        if self.core.config.copId != '':
            if copFn is None:
                raise AttributeError('No such method for company platform')
            else:
                return tokenFn(copFn)(*args, **kwargs)
        elif self.core.config.appId != '':
            if mpFn is None:
                raise AttributeError('No such method for massive platform')
            else:
                return tokenFn(mpFn)(*args, **kwargs)
        else:
            raise AttributeError('You must specific appId or copId before use this method')

class Common(BaseController):
    def __init__(self, core):
        super(Common, self).__init__(core)
        self.mpToken = mpCommon.TokenClass(core)
        self.mpServerList = mpCommon.ServerListClass(core, self.mpToken)
    def update_access_token(self):
        return self.determine_wrapper(self.mpToken.update_access_token,
            qyCommon.update_access_token, needToken=False)
    def access_token(self, fn):
        return self.determine_wrapper(self.mpToken.access_token, 
            qyCommon.access_token, fn,
            needToken=False)
    def get_server_ip(self):
        return self.determine_wrapper(self.mpServerList.get_server_ip, 
            qyCommon.get_server_ip, needToken=False)
    def filter_request(self, request):
        return self.determine_wrapper(self.mpServerList.filter_request, 
            qyCommon.filter_request, request,
            needToken=False)
    def clear_quota(self):
        return self.determine_wrapper(mpCommon.clear_quota, None)
