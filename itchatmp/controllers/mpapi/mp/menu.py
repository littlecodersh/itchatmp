import logging, json

from ..requests import requests
from itchatmp.utils import retry, encode_send_dict
from itchatmp.config import SERVER_URL, COROUTINE
from itchatmp.returnvalues import ReturnValue
from .common import access_token
from ..base.menu import create_producer, get_producer, delete_producer

logger = logging.getLogger('itchatmp')

create = create_producer(SERVER_URL, access_token)

get = get_producer(SERVER_URL, access_token)

delete = delete_producer(SERVER_URL, access_token)

def addconditional(menuDict, autoDecide=False):
    @access_token
    def _add(menuDict, accessToken):
        data = encode_send_dict(menuDict)
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/menu/addconditional?access_token=%s' % (
            SERVER_URL, accessToken), data=data)
        def _wrap_result(result):
            result = ReturnValue(result.json())
            if 'menuid' in result: result['errcode'] = 0
            return result
        r._wrap_result = _wrap_result
        return r
    if not ('button' in menuDict and 'matchrule' in menuDict):
        return ReturnValue({'errcode': 40035})
    if autoDecide and not COROUTINE:
        currentMenu = get()
        for cm in currentMenu.get('conditionalmenu', []):
            if cm.get('button', []) == currentMenu['button'] and \
                    cm.get('matchrule', {}) == currentMenu['matchrule']:
                logger.debug('exists conditional menu with same content')
                return ReturnValue({'errcode': 0})
    return _add(menuDict)
    
@access_token
def delconditional(menuId, accessToken=None):
    r = requests.post('%s/cgi-bin/menu/delconditional?access_token=%s' % (
        SERVER_URL, accessToken), data={'menuid': menuId})
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

@access_token
def trymatch(userId, accessToken=None):
    ''' get menu of specific user
     * userId can be wechat account or openId
    '''
    r = requests.post('%s/cgi-bin/menu/trymatch?access_token=%s' % (
        SERVER_URL, accessToken), data={'user_id': userId})
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

@access_token
def get_current_selfmenu_info(accessToken=None):
    r = requests.get(
        '%s/cgi-bin/menu/get_current_selfmenu_info?access_token=%s'
        % (SERVER_URL, accessToken))
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'selfmenu_info' in result: result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r
