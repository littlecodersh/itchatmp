import logging, json

from ..requests import requests
from itchatmp.utils import retry, encode_send_dict
from itchatmp.content import SERVER_URL
from itchatmp.returnvalues import ReturnValue
from .common import access_token
from ..base.menu import create_producer, get_producer, delete_producer

logger = logging.getLogger('itchatmp')

create = create_producer(SERVER_URL, access_token)

get = get_producer(SERVER_URL, access_token)

delete = delete_producer(SERVER_URL, access_token)

def addconditional(menuDict, autoDecide=True):
    @retry(n=3, waitTime=3)
    @access_token
    def _add(menuDict, accessToken):
        data = encode_send_dict(menuDict)
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/menu/addconditional?access_token=%s' % (
            SERVER_URL, accessToken), data=data).json()
        if 'menuid' in r: r['errcode'] = 0
        return ReturnValue(r)
    if not ('button' in menuDict and 'matchrule' in menuDict):
        return ReturnValue({'errcode': 40035})
    if autoDecide:
        currentMenu = get()
        for cm in currentMenu.get('conditionalmenu', []):
            if 'menuid' in currentMenu:
                if currentMenu['menuid'] == cm['menuid']:
                    logger.debug('exists conditional menu with same menuid')
                    return ReturnValue({'errcode': 0})
            if cm.get('button', []) == currentMenu['button'] and \
                    cm.get('matchrule', {}) == currentMenu['matchrule']:
                logger.debug('exists conditional menu with same content')
                return ReturnValue({'errcode': 0})
    return _add(menuDict)
    
@retry(n=3, waitTime=3)
@access_token
def delconditional(menuId, accessToken=None):
    r = requests.post('%s/cgi-bin/menu/delconditional?access_token=%s' % (
        SERVER_URL, accessToken), json={'menuid': menuId}).json()
    return ReturnValue(r)

@retry(n=3, waitTime=3)
@access_token
def trymatch(userId, accessToken=None):
    ''' get menu of specific user
     * userId can be wechat account or openId
    '''
    r = requests.post('%s/cgi-bin/menu/trymatch?access_token=%s' % (
        SERVER_URL, accessToken), json={'user_id': userId}).json()
    return ReturnValue(r)

@retry(n=3, waitTime=3)
@access_token
def get_current_selfmenu_info(accessToken=None):
    r = requests.get(
        '%s/cgi-bin/menu/get_current_selfmenu_info?access_token=%s'
        % (SERVER_URL, accessToken)).json()
    if 'selfmenu_info' in r: r['errcode'] = 0
    return ReturnValue(r)
