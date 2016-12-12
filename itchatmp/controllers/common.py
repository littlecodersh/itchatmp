from tornado.concurrent import Future

from itchatmp.server import WechatServer
from .mpapi.mp import common as mpCommon
from .mpapi.qy import common as qyCommon

server = WechatServer(None, None, None)

def determine_wrapper(mpFn=None, copFn=None, *args, **kwargs):
    if server.config.copId != '':
        if copFn is None:
            raise AttributeError('No such method for company platform')
        else:
            return copFn(*args, **kwargs)
    elif server.config.appId != '':
        if mpFn is None:
            raise AttributeError('No such method for massive platform')
        else:
            return mpFn(*args, **kwargs)
    else:
        raise AttributeError('You must specific appId or copId before use this method')

def update_access_token():
    return determine_wrapper(mpCommon.update_access_token,
        qyCommon.update_access_token)

def access_token(fn):
    return determine_wrapper(mpCommon.access_token, 
        qyCommon.access_token,
        fn)

def get_server_ip():
    return determine_wrapper(mpCommon.get_server_ip, 
        qyCommon.get_server_ip)

def filter_request(request):
    return determine_wrapper(mpCommon.filter_request, 
        qyCommon.filter_request,
        request)

def clear_quota():
    return determine_wrapper(mpCommon.clear_quota, None)

server.filter_request = filter_request
server.access_token = access_token
server.clear_quota = clear_quota
