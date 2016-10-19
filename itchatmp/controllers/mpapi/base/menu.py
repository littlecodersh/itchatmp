import logging

from ..requests import requests
from itchatmp.utils import retry, encode_send_dict
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

def create_producer(serverUrl, access_token):
    def _create(menuDict, autoDecide=True, agentId=None):
        @retry(n=3, waitTime=3)
        @access_token
        def __create(menuDict, agentId, accessToken):
            data = encode_send_dict(menuDict)
            if data is None: return ReturnValue({'errcode': -10001})
            url = '%s/cgi-bin/menu/create?access_token=%s' % \
                (serverUrl, accessToken)
            if agentId is not None: url += '&agentid=%s' % agentId
            r = requests.post(url, data=data).json()
            return ReturnValue(r)
        if autoDecide:
            currentMenu = get_producer(serverUrl, access_token)()
            if currentMenu.get('menu', {}) == menuDict:
                logger.debug('Menu already exists')
                return ReturnValue({'errcode': 0})
        return __create(menuDict, agentId)
    return _create

def get_producer(serverUrl, access_token):
    @retry(n=3, waitTime=3)
    @access_token
    def _get(agentId=None, accessToken=None):
        url = '%s/cgi-bin/menu/get?access_token=%s' % (serverUrl, accessToken)
        if agentId is not None: url += '&agentid=%s' % agentId
        r = requests.get(url).json()
        if 'menu' in r: r['errcode'] = 0
        return ReturnValue(r)
    return _get

def delete_producer(serverUrl, access_token):
    @retry(n=3, waitTime=3)
    @access_token
    def _delete(agentId=None, accessToken=None):
        url = '%s/cgi-bin/menu/delete?access_token=%s' % (serverUrl, accessToken)
        if agentId is not None: url += '&agentid=%s' % agentId
        r = requests.get(url).json()
        return ReturnValue(r)
    return _delete
