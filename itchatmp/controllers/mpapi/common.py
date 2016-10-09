import logging

import requests

from itchatmp.content import SERVER_URL
from itchatmp.server import WechatServer
from itchatmp.utils import retry
from itchatmp.controllers.returnvalues import ReturnValue
from .accesstoken import access_token

logger = logging.getLogger('itchatmp')

__server = WechatServer.instance()

@access_token
def get_server_ip(accessToken=None):
    url = '%s/cgi-bin/getcallbackip?access_token=%s' % \
        (SERVER_URL, accessToken)
    r = requests.get(url).json()
    if 'ip_list' in r: r['errcode'] = 0
    return ReturnValue(r)
