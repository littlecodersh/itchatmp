import logging, json, copy

from ..requests import requests
from itchatmp.utils import retry, encode_send_dict
from itchatmp.config import SERVER_URL
from itchatmp.content import (
    IMAGE, VOICE, VIDEO, THUMB, TEXT, NEWS, CARD)
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

def set_industry(id1, id2, accessToken=None):
    ''' set industry for your massive platform '''
    data = {'industry_id1': str(id1), 'industry_id2': str(id2)}
    r = requests.post('%s/cgi-bin/template/api_set_industry?access_token=%s' % 
        (SERVER_URL, accessToken), data=encode_send_dict(data))
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def get_industry(accessToken=None):
    ''' get industry of your massive platform '''
    r = requests.get('%s/cgi-bin/template/get_industry?access_token=%s' % 
        (SERVER_URL, accessToken))
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'primary_industry' in result:
            result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r

def add_template(templateId, accessToken=None):
    ''' add template for your massive platform '''
    data = {'template_id_short': templateId}
    r = requests.post('%s/cgi-bin/template/api_add_template?access_token=%s' % 
        (SERVER_URL, accessToken), data=encode_send_dict(data))
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def delete_templates(templateId, accessToken=None):
    ''' delete template of your massive platform '''
    data = {'template_id': templateId}
    r = requests.post('%s/cgi-bin/template/del_private_template?access_token=%s' % 
        (SERVER_URL, accessToken), data=encode_send_dict(data))
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def get_templates(accessToken=None):
    ''' get templates of your massive platform '''
    r = requests.get('%s/cgi-bin/template/get_all_private_template?access_token=%s' % 
        (SERVER_URL, accessToken))
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'template_list' in result: result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r

def send(templateId, msgDict, toUserId, accessToken=None):
    ''' send template to your massive platform users '''
    msgDict = copy.deepcopy(msgDict)
    msgDict['touser'], msgDict['template_id'] = toUserId, templateId
    data = encode_send_dict(msgDict)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/template/del_private_template?access_token=%s' % 
        (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r
