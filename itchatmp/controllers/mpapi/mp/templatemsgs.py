import logging, json, copy

from ..requests import requests
from .common import access_token
from itchatmp.utils import retry, encode_send_dict
from itchatmp.content import (SERVER_URL,
    IMAGE, VOICE, VIDEO, THUMB, TEXT, NEWS, CARD)
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

@retry(n=3, waitTime=3)
@access_token
def set_industry(id1, id2, accessToken=None):
    ''' set industry for your massive platform '''
    data = {'industry_id1': str(id1), 'industry_id2': str(id2)}
    r = requests.post('%s/cgi-bin/template/api_set_industry?access_token=%s' % 
        (SERVER_URL, accessToken), data=encode_send_dict(data)).json()
    return ReturnValue(r)

@retry(n=3, waitTime=3)
@access_token
def get_industry(accessToken=None):
    ''' get industry of your massive platform '''
    r = requests.get('%s/cgi-bin/template/get_industry?access_token=%s' % 
        (SERVER_URL, accessToken)).json()
    if 'primary_industry' in r: r['errcode'] = 0
    return ReturnValue(r)

@retry(n=3, waitTime=3)
@access_token
def add_template(templateId, accessToken=None):
    ''' add template for your massive platform '''
    data = {'template_id_short': templateId}
    r = requests.post('%s/cgi-bin/template/api_add_template?access_token=%s' % 
        (SERVER_URL, accessToken), data=encode_send_dict(data)).json()
    return ReturnValue(r)

@retry(n=3, waitTime=3)
@access_token
def delete_templates(templateId, accessToken=None):
    ''' delete template of your massive platform '''
    data = {'template_id': templateId}
    r = requests.post('%s/cgi-bin/template/del_private_template?access_token=%s' % 
        (SERVER_URL, accessToken), data=encode_send_dict(data)).json()
    return ReturnValue(r)

@retry(n=3, waitTime=3)
@access_token
def get_templates(accessToken=None):
    ''' get templates of your massive platform '''
    r = requests.get('%s/cgi-bin/template/get_all_private_template?access_token=%s' % 
        (SERVER_URL, accessToken)).json()
    if 'template_list' in r: r['errcode'] = 0
    return ReturnValue(r)

@retry(n=3, waitTime=3)
@access_token
def send(templateId, msgDict, toUserId, accessToken=None):
    ''' send template to your massive platform users '''
    msgDict = copy.deepcopy(msgDict)
    msgDict['touser'], msgDict['template_id'] = toUserId, templateId
    data = encode_send_dict(msgDict)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/template/del_private_template?access_token=%s' % 
        (SERVER_URL, accessToken), data=data).json()
    return ReturnValue(r)
