import logging

from ..requests import requests
from itchatmp.config import COROUTINE
from itchatmp.returnvalues import ReturnValue
from itchatmp.utils import retry, encode_send_dict

logger = logging.getLogger('itchatmp')

def create_producer(serverUrl):
    def _create(menuDict, agentId=None, accessToken=None):
        data = encode_send_dict(menuDict)
        if data is None: return ReturnValue({'errcode': -10001})
        url = '%s/cgi-bin/menu/create?access_token=%s' % \
            (serverUrl, accessToken)
        if agentId is not None: url += '&agentid=%s' % agentId
        r = requests.post(url, data=data)
        def _wrap_result(result):
            return ReturnValue(result.json())
        r._wrap_result = _wrap_result
        return r
    return _create

def get_producer(serverUrl):
    def _get(agentId=None, accessToken=None):
        url = '%s/cgi-bin/menu/get?access_token=%s' % (serverUrl, accessToken)
        if agentId is not None: url += '&agentid=%s' % agentId
        r = requests.get(url)
        def _wrap_result(result):
            result = result.json()
            if 'menu' in result: result['errcode'] = 0
            return ReturnValue(result)
        r._wrap_result = _wrap_result
        return r
    return _get

def delete_producer(serverUrl):
    def _delete(agentId=None, accessToken=None):
        url = '%s/cgi-bin/menu/delete?access_token=%s' % (serverUrl, accessToken)
        if agentId is not None: url += '&agentid=%s' % agentId
        r = requests.get(url)
        def _wrap_result(result):
            return ReturnValue(result.json())
        r._wrap_result = _wrap_result
        return r
    return _delete
