import functools, logging, time

import requests

from itchatmp.server import WechatServer
from itchatmp.utils import retry
from itchatmp.models.accesstoken import get_access_token, store_access_token
from itchatmp.controllers.returnvalues import parse_return_value

logger = logging.getLogger('itchatmp')

__server = WechatServer.instance()

@retry(n=3, waitTime=3)
def update_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token'\
        '?grant_type=client_credential&appid=%s&secret=%s'
    url = url % (__server.config.appId, __server.config.appSecret)
    r = requests.get(url).json()
    if 'access_token' in r:
        store_access_token(r['access_token'], r['expires_in'])
        return True
    else:
        r = parse_return_value(r)
        logger.debug('Failed to get token: %r' %r)
        return r

def access_token(fn):
    @functools.wraps(fn)
    def _access_token(*args, **kwargs):
        accessToken, expireTime = get_access_token()
        if expireTime < time.time():
            updateResult = update_access_token()
            if not updateResult: return updateResult
            accessToken, expireTime = get_access_token()
        kwargs['accessToken'] = accessToken
        return fn(*args, **kwargs)
    return _access_token
