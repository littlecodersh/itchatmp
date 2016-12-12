from itchatmp.config import COMPANY_URL
from itchatmp.returnvalues import ReturnValue
from itchatmp.utils import retry
from ..base.common import (update_access_token_producer,
    access_token_producer, filter_request_producer)
from ..requests import requests

__all__ = ['update_access_token', 'access_token', 'get_server_ip', 'filter_request']

update_access_token = update_access_token_producer(
    COMPANY_URL + '/cgi-bin/gettoken?corpid=%s&corpsecret=%s',
    lambda x: x.config.copId)

access_token = access_token_producer(update_access_token)

def get_server_ip():
    @access_token
    def _get_server_ip(accessToken=None):
        url = '%s/cgi-bin/getcallbackip?access_token=%s' % \
            (COMPANY_URL, accessToken)
        r = requests.get(url).json()
        if 'ip_list' in r:
            r['errcode'] = 0
            for i, v in enumerate(r['ip_list']):
                r['ip_list'][i] = v[:v.rfind('/')]
        return ReturnValue(r)
    return _get_server_ip()

filter_request = filter_request_producer(get_server_ip)
