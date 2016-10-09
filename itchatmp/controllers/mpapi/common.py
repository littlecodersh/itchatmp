import logging, time, threading
from datetime import datetime, timedelta

import requests

from itchatmp.content import SERVER_URL
from itchatmp.server import WechatServer
from itchatmp.utils import retry
from itchatmp.controllers.returnvalues import ReturnValue
from .accesstoken import access_token

logger = logging.getLogger('itchatmp')

__server = WechatServer.instance()
__serverList = None

@access_token
def get_server_ip(accessToken=None):
    url = '%s/cgi-bin/getcallbackip?access_token=%s' % \
        (SERVER_URL, accessToken)
    r = requests.get(url).json()
    if 'ip_list' in r:
        r['errcode'] = 0
        for i, v in enumerate(r['ip_list']):
            r['ip_list'][i] = v[:v.rfind('/')]
    return ReturnValue(r)

def set_server_list():
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

def filter_request(request):
    global __serverList
    if __serverList is None:
        t = threading.Thread(target=set_server_list)
        t.setDaemon = True
        t.start()
        def clear_server_list():
            __serverList = None
        __server.ioLoop.call_later(
            (datetime.replace(datetime.now() + timedelta(days=1), 
            hour=0, minute=5, second=0) - datetime.now()).seconds,
            lambda: clear_server_list())
    if not __serverList: return True
    print(request.remote_ip in __serverList)
    print(request.remote_ip)
    return request.remote_ip in __serverList
__server._filter_request = filter_request
