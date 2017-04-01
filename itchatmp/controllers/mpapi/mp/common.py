from requests import get

from itchatmp.config import SERVER_URL, COROUTINE
from itchatmp.returnvalues import ReturnValue
from itchatmp.utils import retry
from ..base.common import TokenClass as _TokenClass, ServerListClass
from ..requests import requests

class TokenClass(_TokenClass):
    def __init__(self, core):
        _TokenClass.__init__(self, core, SERVER_URL + 
            '/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s',
            lambda x: x.config.appId)

def clear_quota(accessToken=None):
    data = {'appid': server.config.appId}
    r = requests.post('%s/cgi-bin/clear_quota?access_token=%s' %
        (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        return ReturnValue(result.json())
    return r
