import functools, logging, time, threading, traceback
from datetime import datetime, timedelta

from requests.models import Response
from requests.sessions import session
from tornado import gen

from ..requests import requests
from itchatmp.config import COROUTINE
from itchatmp.server import WechatServer
from itchatmp.utils import retry
from itchatmp.returnvalues import ReturnValue

__all__ = ['update_access_token_producer', 'access_token', 'filter_request']

logger = logging.getLogger('itchatmp')

__server = WechatServer(None, None, None)
__AUTO_MAINTAIN = False
__serverList = None
__session = session()
__session.verify = False
get = __session.get

def auto_maintain_thread(firstCallResult=None, tokenUrl=None, appIdFn=None):
    r = firstCallResult or update_access_token_producer(tokenUrl, appIdFn, True)()
    if not r:
        __server.ioLoop.call_later(
            (datetime.replace(datetime.now() + timedelta(days=1), 
            hour=0, minute=5, second=0) - datetime.now()).seconds,
            maintain_access_token,
            None, tokenUrl, appIdFn)
    else:
        __server.ioLoop.call_later(r['expires_in'] - 30,
            maintain_access_token,
            None, tokenUrl, appIdFn)

def maintain_access_token(firstCallResult=None, tokenUrl=None, appIdFn=None):
    t = threading.Thread(target=auto_maintain_thread,
        args=(firstCallResult, tokenUrl, appIdFn))
    t.setDaemon(True); t.start()

def update_access_token_producer(tokenUrl, appIdFn, forceSync=False):
    ''' function to update access token
     * auto-maintain begins when this function is called for the first time
       - of course, if isWsgi or haven't started, auto-maintain will not start
     * If auto-maintain failed, it will restart tomorrow 0004h:30
     * will return ReturnValue object (equals to True) if success
     * will return ReturnValue object (equals to False) if fail
     * ReturnValue object contains why update failed
    '''
    if COROUTINE and not forceSync:
        @gen.coroutine
        def _update_access_token():
            global __AUTO_MAINTAIN
            url = tokenUrl % (appIdFn(__server), __server.config.appSecret)
            r = (yield requests.get(url)).json()
            if 'access_token' in r:
                __server.atStorage.store_access_token(
                    r['access_token'], int(time.time()) + r['expires_in'])
                r['errcode'] = 0
                r = ReturnValue(r)
            else:
                r = ReturnValue(r)
                logger.debug('Failed to get token: %s' %r)
            if not __AUTO_MAINTAIN and not __server.isWsgi:
                __AUTO_MAINTAIN = True
                maintain_access_token(r, tokenUrl, appIdFn)
            raise gen.Return(r)
        return _update_access_token
    else:
        def _update_access_token():
            global __AUTO_MAINTAIN
            url = tokenUrl % (appIdFn(__server), __server.config.appSecret)
            r = get(url).json()
            if 'access_token' in r:
                __server.atStorage.store_access_token(
                    r['access_token'], int(time.time()) + r['expires_in'])
                r['errcode'] = 0
                r = ReturnValue(r)
            else:
                r = ReturnValue(r)
                logger.debug('Failed to get token: %s' %r)
            if not __AUTO_MAINTAIN and not __server.isWsgi:
                __AUTO_MAINTAIN = True
                maintain_access_token(r, tokenUrl, appIdFn)
            return r
        return _update_access_token

def access_token_producer(tokenFn, forceSync=False):
    ''' wrapper for functions need accessToken
        accessToken should be a key argument of the wrapped fn
        ..code:: python
             @access_token
             def fn(a, b, c, accessToken=False):
                 pass
        if accessToken is not successfully fetched, wrapped fn will return why
        There's a very tricky thing about this decorator:
            You need to return a requests.models.Response object
            And set _wrap_result of the object to format result
    '''
    if COROUTINE and not forceSync:
        def _access_token(fn):
            @gen.coroutine
            @functools.wraps(fn)
            def __access_token(*args, **kwargs):
                accessToken, expireTime = __server.atStorage.get_access_token()
                if expireTime < time.time():
                    updateResult = yield tokenFn()
                    if not updateResult:
                        raise gen.Return(updateResult)
                    accessToken, expireTime = __server.atStorage.get_access_token()
                kwargs['accessToken'] = accessToken
                future = fn(*args, **kwargs)
                r = yield future
                try:
                    errcode = r.json().get('errcode')
                    isTokenTimeout = errcode == 40014
                except:
                    isTokenTimeout = False
                if isinstance(r, Response) and isTokenTimeout:
                    updateResult = yield tokenFn()
                    if not updateResult:
                        raise gen.Return(updateResult)
                    accessToken, expireTime = __server.atStorage.get_access_token()
                    kwargs['accessToken'] = accessToken
                    future = fn(*args, **kwargs)
                    r = yield future
                wrap_fn = getattr(future, '_wrap_result', None)
                if wrap_fn is not None:
                    try:
                        r = wrap_fn(r)
                    except:
                        r = ReturnValue({'errcode': -10005, 'errmsg': traceback.format_exc()})
                raise gen.Return(r)
            return __access_token
        return _access_token
    else:
        def _access_token(fn):
            @functools.wraps(fn)
            def __access_token(*args, **kwargs):
                accessToken, expireTime = __server.atStorage.get_access_token()
                if expireTime < time.time():
                    updateResult = tokenFn()
                    if not updateResult:
                        return updateResult
                    accessToken, expireTime = __server.atStorage.get_access_token()
                kwargs['accessToken'] = accessToken
                r = fn(*args, **kwargs)
                try:
                    errcode = r.json().get('errcode')
                    isTokenTimeout = errcode == 40014
                except:
                    isTokenTimeout = False
                if isinstance(r, Response) and isTokenTimeout:
                    updateResult = tokenFn()
                    if not updateResult:
                        return updateResult
                    accessToken, expireTime = __server.atStorage.get_access_token()
                    kwargs['accessToken'] = accessToken
                    r = fn(*args, **kwargs)
                wrap_fn = getattr(r, '_wrap_result', None)
                if wrap_fn is not None:
                    try:
                        r = wrap_fn(r)
                    except:
                        r = ReturnValue({'errcode': -10005, 'errmsg': traceback.format_exc()})
                return r
            return __access_token
        return _access_token

def set_server_list(get_server_ip):
    global __serverList
    __serverList = []
    serverList, fetchTime = __server.atStorage.get_server_list()
    if fetchTime < time.mktime(datetime.replace(datetime.now(),
        hour=0, minute=0, second=0).timetuple()):
        r = get_server_ip()
        if not r: logger.debug(r)
        __serverList = r.get('ip_list', [])
        __server.atStorage.store_server_list(__serverList, time.time())
    else:
        __serverList = serverList

def filter_request_producer(get_server_ip):
    def filter_request(request):
        global __serverList
        if __serverList is None:
            t = threading.Thread(target=set_server_list, args=(get_server_ip,))
            t.setDaemon = True
            t.start()
            def clear_server_list():
                __serverList = None
            __server.ioLoop.call_later(
                (datetime.replace(datetime.now() + timedelta(days=1), 
                hour=0, minute=5, second=0) - datetime.now()).seconds,
                lambda: clear_server_list())
        if not __serverList:
            logger.debug('Server list is loading, so ignore verifying once.')
            return True
        return request.remote_ip in __serverList
    return filter_request
