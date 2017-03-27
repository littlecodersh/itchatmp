from weakref import ref

from tornado.concurrent import Future

from itchatmp.utils import CoreMixin
from .mpapi.mp import common as mpCommon
from .mpapi.qy import common as qyCommon

class BaseController(CoreMixin):
    def determine_wrapper(self, mpFn=None, copFn=None, *args, **kwargs):
        if self.core.config.copId != '':
            if copFn is None:
                raise AttributeError('No such method for company platform')
            else:
                return copFn(self, *args, **kwargs)
        elif self.core.config.appId != '':
            if mpFn is None:
                raise AttributeError('No such method for massive platform')
            else:
                return mpFn(self, *args, **kwargs)
        else:
            raise AttributeError('You must specific appId or copId before use this method')

class Common(BaseController):
    def __init__(self, core):
        super(Common, self).__init__(core)
        self.mpToken = mpCommon.TokenClass(core)
        self.mpServerList = mpCommon.ServerListClass(core)
    def update_access_token(self):
        return self.determine_wrapper(self.mpToken.update,
            qyCommon.update_access_token)
    def access_token(self, fn):
        return self.determine_wrapper(self.mpToken._accessTokenFunction, 
            qyCommon.access_token,
            fn)
    def get_server_ip(self):
        return self.determine_wrapper(self.mpServerList._serverIpFn, 
            qyCommon.get_server_ip)
    def filter_request(self, request):
        return self.determine_wrapper(self.mpServerList.filter_request, 
            qyCommon.filter_request,
            request)
    def clear_quota(self):
        return self.determine_wrapper(mpCommon.clear_quota, None)
