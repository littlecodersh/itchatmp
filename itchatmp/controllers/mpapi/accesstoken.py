import functools, logging, time
import threading
from datetime import datetime, timedelta

import requests

from itchatmp.content import SERVER_URL
from itchatmp.server import WechatServer
from itchatmp.utils import retry
from itchatmp.models.accesstoken import get_access_token, store_access_token
from itchatmp.controllers.returnvalues import ReturnValue

__all__ = ['update_access_token', 'access_token']

logger = logging.getLogger('itchatmp')

__server = WechatServer.instance()
__AUTO_MAINTAIN = False

def auto_maintain_thread(firstCallResult=None):
    r = firstCallResult or update_access_token()
    if not r:
        __server.ioLoop.call_later(
            (datetime.replace(datetime.now() + timedelta(days=1), 
            hour=0, minute=5, second=0) - datetime.now()).seconds,
            maintain_access_token)
    else:
        __server.ioLoop.call_later(r['expires_in'] - 30,
            maintain_access_token)

def maintain_access_token(firstCallResult=None):
    t = threading.Thread(target=auto_maintain_thread,
        kwargs={'firstCallResult': firstCallResult})
    t.setDaemon(True); t.start()

@retry(n=3, waitTime=3)
def update_access_token():
    ''' function to update access token
     * auto-maintain begins when this function is called for the first time
     * If auto-maintain failed, it will restart tomorrow 0004h:30
     * will return ReturnValue object (equals to True) if success
     * will return ReturnValue object (equals to False) if fail
     * ReturnValue object contains why update failed
    '''
    global __AUTO_MAINTAIN
    url = '%s/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % \
        (SERVER_URL, __server.config.appId, __server.config.appSecret)
    r = requests.get(url).json()
    if 'access_token' in r:
        store_access_token(r['access_token'], int(time.time()) + r['expires_in'])
        r['errcode'] = 0
        r = ReturnValue(r)
    else:
        r = ReturnValue(r)
        logger.debug('Failed to get token: %s' %r)
    if not __AUTO_MAINTAIN:
        __AUTO_MAINTAIN = True
        maintain_access_token(firstCallResult=r)
    return r

def access_token(fn):
    ''' wrapper for functions need accessToken
     * accessToken should be a key argument of the wrapped fn
       ..code:: python
            def fn(a, b, c, accessToken=False):
                pass
     * if accessToken is not successfully fetched, wrapped fn will return why
    '''
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
