from itchatmp.server import WechatServer
from .mp import common as mpCommon
from .qy import common as qyCommon

__server = WechatServer.instance()

def determine_wrapper(mpFn=None, copFn=None, *args, **kwargs):
    if __server.config.copId != '':
        if copFn is None:
            raise AttributeError('No such method for company platform')
        else:
            return copFn(*args, **kwargs)
    elif __server.config.appId != '':
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

__server._filter_request = filter_request
