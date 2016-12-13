from requests import get

from itchatmp.config import SERVER_URL, COROUTINE
from itchatmp.returnvalues import ReturnValue
from itchatmp.server import WechatServer
from itchatmp.utils import retry
from ..base.common import (update_access_token_producer,
    access_token_producer, filter_request_producer)
from ..requests import requests

__all__ = ['update_access_token', 'access_token', 'get_server_ip', 'filter_request', 'clear_quota']

server = WechatServer(None, None, None)

update_access_token = update_access_token_producer(
    SERVER_URL + '/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s',
    lambda x: x.config.appId)

access_token = access_token_producer(update_access_token)

def get_server_ip_producer(forceSync=False):
    if COROUTINE and not forceSync:
        at = access_token
        requests_get = requests.get
    else:
        token_fn = update_access_token_producer(
            SERVER_URL + '/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s',
            lambda x: x.config.appId, forceSync=True)
        at = access_token_producer(token_fn, forceSync=True)
        requests_get = get
    @at
    def _get_server_ip(accessToken=None):
        url = '%s/cgi-bin/getcallbackip?access_token=%s' % \
            (SERVER_URL, accessToken)
        r = requests_get(url)
        def _wrap_result(result):
            result = ReturnValue(result.json())
            if 'ip_list' in result:
                result['errcode'] = 0
                for i, v in enumerate(result['ip_list']):
                    result['ip_list'][i] = v[:v.rfind('/')]
            return result
        r._wrap_result = _wrap_result
        return r
    return _get_server_ip

get_server_ip = get_server_ip_producer()

filter_request = filter_request_producer(get_server_ip_producer(True))

@access_token
def clear_quota(accessToken=None):
    data = {'appid': server.config.appId}
    r = requests.post('%s/cgi-bin/clear_quota?access_token=%s' %
        (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        return ReturnValue(result.json())
    return r
