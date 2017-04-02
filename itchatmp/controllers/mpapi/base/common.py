import functools, logging, time, threading, traceback
from datetime import datetime, timedelta

from requests import get
from requests.models import Response
from requests.sessions import session
from tornado import gen

from ..requests import requests
from itchatmp.config import COROUTINE
from itchatmp.utils import retry, CoreMixin
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

class TokenClass(CoreMixin):
    def __init__(self, core, tokenUrl, appIdFn):
        super(TokenClass, self).__init__(core)
        self.tokenUrl, self.appIdFn = tokenUrl, appIdFn
        self._session = session()
        self._session.verify = False
        self._autoMaintain = False
        self._tokenFunction = self.token_function_producer()
        self._syncTokenFunction = self.token_function_producer(True)
        self._accessTokenFunction = self.access_token_producer()
        self._syncAccessTokenFunction = self.access_token_producer(True)
    def token_function_producer(self, forceSync=False):
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
                url = self.tokenUrl % (self.appIdFn(self.core), self.core.config.appSecret)
                r = (yield requests.get(url)).json()
                if 'access_token' in r:
                    self.core.atStorage.store_access_token(
                        r['access_token'], int(time.time()) + r['expires_in'])
                    r['errcode'] = 0
                    r = ReturnValue(r)
                else:
                    r = ReturnValue(r)
                    logger.debug('Failed to get token: %s' %r)
                if not self._autoMaintain and not self.core.isWsgi:
                    self._autoMaintain = True
                    self.maintain_access_token(r)
                raise gen.Return(r)
            return _update_access_token
        else:
            def _update_access_token():
                url = self.tokenUrl % (self.appIdFn(self.core), self.core.config.appSecret)
                r = self._session.get(url).json()
                if 'access_token' in r:
                    self.core.atStorage.store_access_token(
                        r['access_token'], int(time.time()) + r['expires_in'])
                    r['errcode'] = 0
                    r = ReturnValue(r)
                else:
                    r = ReturnValue(r)
                    logger.debug('Failed to get token: %s' %r)
                if not self._autoMaintain and not self.core.isWsgi:
                    self._autoMaintain = True
                    self.maintain_access_token(r)
                return r
            return _update_access_token
    def maintain_thread(self, firstCallResult=None):
        ''' thread to update token and
        register next update event into event loop '''
        r = firstCallResult or self._syncTokenFunction()
        if not r:
            self.core.ioLoop.call_later(
                (datetime.replace(datetime.now() + timedelta(days=1), 
                hour=0, minute=5, second=0) - datetime.now()).seconds,
                self.maintain_access_token, None)
        else:
            self.core.ioLoop.call_later(r['expires_in'] - 30,
                self.maintain_access_token, None)
    def maintain_access_token(self, firstCallResult=None):
        t = threading.Thread(target=auto_maintain_thread,
            args=(firstCallResult,))
        t.setDaemon(True)
        t.start()
    def access_token_producer(self, forceSync=False):
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
                    accessToken, expireTime = self.core.atStorage.get_access_token()
                    if expireTime < time.time():
                        updateResult = yield self.update_access_token()
                        if not updateResult:
                            raise gen.Return(updateResult)
                        accessToken, expireTime = self.core.atStorage.get_access_token()
                    kwargs['accessToken'] = accessToken
                    future = fn(*args, **kwargs)
                    if gen.is_future(future):
                        r = yield future
                    else:
                        r = future
                    try:
                        errcode = r.json().get('errcode')
                        isTokenTimeout = errcode == 40014
                    except:
                        isTokenTimeout = False
                    if isinstance(r, Response) and isTokenTimeout:
                        updateResult = yield self.update_access_token()
                        if not updateResult:
                            raise gen.Return(updateResult)
                        accessToken, expireTime = self.core.atStorage.get_access_token()
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
                    accessToken, expireTime = self.core.atStorage.get_access_token()
                    if expireTime < time.time():
                        updateResult = self.update_access_token()
                        if not updateResult:
                            return updateResult
                        accessToken, expireTime = self.core.atStorage.get_access_token()
                    kwargs['accessToken'] = accessToken
                    r = fn(*args, **kwargs)
                    try:
                        errcode = r.json().get('errcode')
                        isTokenTimeout = errcode == 40014
                    except:
                        isTokenTimeout = False
                    if isinstance(r, Response) and isTokenTimeout:
                        updateResult = self.update_access_token()
                        if not updateResult:
                            return updateResult
                        accessToken, expireTime = self.core.atStorage.get_access_token()
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
    def update_access_token(self):
        return self._tokenFunction()
    def access_token(self, fn):
        return self._accessTokenFunction(fn)

class ServerListClass(CoreMixin):
    def __init__(self, core, tokenClass, serverUrl):
        super(ServerListClass, self).__init__(core)
        self.tokenClass = tokenClass
        self.serverUrl = serverUrl
        self._serverList = None
        self._serverIpFn = self.get_server_ip_producer()
        self._syncServerIpFn = self.get_server_ip_producer(True)
    def set_server_list(self):
        self._serverList = []
        serverList, fetchTime = self.core.atStorage.get_server_list()
        if fetchTime < time.mktime(datetime.replace(datetime.now(),
            hour=0, minute=0, second=0).timetuple()):
            r = self._serverIpFn()
            if not r:
                logger.debug(r)
            else:
                self._serverList = r.get('ip_list', [])
                self.core.atStorage.store_server_list(self._serverList, time.time())
        else:
            self._serverList = serverList
    def get_server_ip_producer(self, forceSync=False):
        if COROUTINE and not forceSync:
            access_token = self.tokenClass._accessTokenFunction
            requests_get = requests.get
        else:
            access_token = self.tokenClass._syncAccessTokenFunction
            requests_get = get
        @access_token
        def _get_server_ip(accessToken=None):
            url = self.serverUrl % accessToken
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
    def get_server_ip(self):
        return self._serverIpFn()
    def filter_request(self, request):
        if self._serverList is None:
            t = threading.Thread(target=self.set_server_list)
            t.setDaemon = True
            t.start()
            def clear_server_list():
                self._serverList = None
            self.core.ioLoop.call_later(
                (datetime.replace(datetime.now() + timedelta(days=1), 
                hour=0, minute=5, second=0) - datetime.now()).seconds,
                clear_server_list)
        if not self._serverList:
            logger.debug('Server list is loading, so ignore verifying once.')
            return True
        return request.remote_ip in self._serverList
