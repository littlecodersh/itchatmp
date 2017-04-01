import logging

from ..requests import requests
from .common import access_token
from itchatmp.config import COMPANY_URL
from itchatmp.content import (
    IMAGE, VOICE, VIDEO, MUSIC, TEXT, NEWS, CARD)
from itchatmp.utils import retry, encode_send_dict
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

@access_token
def authorize_user(userId, accessToken=None):
    params = {
        'access_token': accessToken,
        'userid': userId, }
    r = requests.get('%s/cgi-bin/user/authsucc' % COMPANY_URL, params=params).json()
    return ReturnValue(r)

@access_token
def create_department(name, parentId=1, order=None, id=None, accessToken=None):
    data = {
        'name': name,
        'parentid': parentId, }
    if order is not None: data['order'] = order
    if id is not None: data['id'] = id
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/department/create?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def update_department(id, name=None, parentId=None, order=None, accessToken=None):
    data = {'id': id}
    if name is not None: data['name'] = name
    if parentId is not None: data['parentid'] = parentId
    if order is not None: data['order'] = order
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/department/update?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def delete_department(id, accessToken=None):
    params = {
        'access_token': accessToken,
        'id': id, }
    r = requests.get('%s/cgi-bin/department/delete' % COMPANY_URL, params=params).json()
    return ReturnValue(r)

@access_token
def get_departments(parentId, accessToken=None):
    params = {
        'access_token': accessToken,
        'id': parentId, }
    r = requests.get('%s/cgi-bin/department/list' % COMPANY_URL, params=params).json()
    return ReturnValue(r)

@access_token
def create_user(userId, name, departmentIdList,
        position=None, mobile=None, gender=None, email=None,
        weixinId=None, headImgId=None, extAttr=None,
        accessToken=None):
    data = {
        'userid': userId               , 'name': name         ,
        'department': departmentIdList , 'position': position ,
        'mobile': mobile               , 'gender': gender     ,
        'email': email                 , 'weixinid': weixinId ,
        'avatar_mediaid': headImgId    , 'extattr': extAttr   , }
    for k in list(data):
        if data[k] is None: del data[k]
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/user/create?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def update_user(userId, name=None, departmentIdList=None,
        position=None, mobile=None, gender=None, email=None,
        weixinId=None, headImgId=None, extAttr=None,
        accessToken=None):
    data = {
        'userid': userId               , 'name': name         ,
        'department': departmentIdList , 'position': position ,
        'mobile': mobile               , 'gender': gender     ,
        'email': email                 , 'weixinid': weixinId ,
        'avatar_mediaid': headImgId    , 'extattr': extAttr   , }
    for k in list(data):
        if data[k] is None: del data[k]
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/user/update?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def delete_users(userId, accessToken=None):
    ''' delete user using userId
     * userId can be a list or only one userId
    '''
    if isinstance(userId, list):
        data = {'useridlist': userId}
        data = encode_send_dict(data)
        if data is None: return ReturnValue({'errcode': -10001})
        url = '%s/cgi-bin/department/batchdelete?access_token=%s' % (COMPANY_URL, accessToken)
        r = requests.post(url, data=data).json()
    else:
        params = {
            'access_token': accessToken,
            'userid': userId, }
        url = '%s/cgi-bin/department/delete'
        r = requests.get(url % COMPANY_URL, params=params).json()
    return ReturnValue(r)

def get_user_info(userId):
    ''' get info of a user or a list of users
     * userId can be a list or only one userId
     * this is for creating api similiar to massive platform
    '''
    @access_token
    def _get_user_info(userId):
        params = {
            'access_token': accessToken,
            'userid': userId, }
        r = requests.get('%s/cgi-bin/user/get' % COMPANY_URL, params=params).json()
        return ReturnValue(r)
    if isinstance(userId, list):
        userDict = {'user_info_list': []}
        for id in userId:
            r = _get_user_info(id)
            if r:
                userDict['user_info_list'].append(r)
            else:
                userDict['errcode'] = r['errcode']
                userDict['errmsg'] = r['errmsg']
                break
        return ReturnValue(userDict)
    else:
        return _get_user_info(userId)

@access_token
def get_users(nextOpenId='', departmentId=None, fetchChild=False, status=4, accessToken=None):
    ''' get users of the department
     * nextOpenId is for mp api
    '''
    if departmentId is None:
        return ReturnValue({'errcode': 40035, 'errmsg': 'departmentId must be set',})
    params = {
        'access_token'  : accessToken,
        'department_id' : departmentId,
        'fetch_child'   : int(fetchChild),
        'status'        : status, }
    r = requests.get('%s/cgi-bin/user/simplelist' % SERVER_URL, params=params).json()
    return ReturnValue(r)

@access_token
def get_detailed_users(nextOpenId='',
        departmentId=None, fetchChild=False, status=4, accessToken=None):
    ''' get users of the department
     * nextOpenId is for mp api
    '''
    if departmentId is None:
        return ReturnValue({'errcode': 40035, 'errmsg': 'departmentId must be set',})
    params = {
        'access_token'  : accessToken,
        'department_id' : departmentId,
        'fetch_child'   : int(fetchChild),
        'status'        : status, }
    r = requests.get('%s/cgi-bin/user/list' % SERVER_URL, params=params).json()
    return ReturnValue(r)

@access_token
def create_tag(name, id=None, accessToken=None):
    data = {'tagname': name}
    if id is not None: data['tagid'] = id
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/tag/create?access_token=%s'
        % (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def get_tags(accessToken=None):
    r = requests.get('%s/cgi-bin/tag/list?access_token=%s'
        % (SERVER_URL, accessToken)).json()
    return ReturnValue(r)

@access_token
def update_tag(id, name, accessToken=None):
    data = encode_send_dict({'tagid': id, 'tagname': name, })
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/tag/update?access_token=%s'
        % (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def delete_tag(id, accessToken=None):
    params = {
        'access_token': accessToken,
        'tagid': id, }
    r = requests.get('%s/cgi-bin/tag/delete' % COMPANY_URL, params=params).json()
    return ReturnValue(r)

@access_token
def get_users_of_tag(id, nextOpenId='', accessToken=None):
    params = {
        'access_token': accessToken,
        'tagid': id, }
    r = requests.get('%s/cgi-bin/tag/get' % COMPANY_URL, params=params).json()
    return ReturnValue(r)

@access_token
def add_users_into_tag(id, userIdList=None, partyList=None, accessToken=None):
    if not (userIdList or partyList):
        return ReturnValue({'errcode': 40035,
            'errmsg': 'either userId or partyList should be set'})
    data = {'tagid': id}
    if userIdList:
        data['userlist'] = userIdList
    if partyList:
        data['partylist'] = partyList
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/tag/addtagusers?access_token=%s'
        % (COMPANY_URL, accessToken), data=data).json()
    if 'invalidlist' in r or 'invalidparty' in r: r['errcode'] = 40070
    return ReturnValue(r)

@access_token
def delete_users_of_tag(id, userIdList=None, partyList=None, accessToken=None):
    if not (userIdList or partyList):
        return ReturnValue({'errcode': 40035,
            'errmsg': 'either userId or partyList should be set'})
    data = {'tagid': id}
    if userIdList:
        data['userlist'] = userIdList
    if partyList:
        data['partylist'] = partyList
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/tag/deltagusers?access_token=%s'
        % (COMPANY_URL, accessToken), data=data).json()
    if 'invalidlist' in r or 'invalidparty' in r: r['errcode'] = 40070
    return ReturnValue(r)

# __server
def upload_contract(csvMediaId, callbackUrl, method='sync'):
    ''' update users with uploaded csv
     * method can be syncuser, replaceuser, replaceparty
    '''
    if method not in ('syncuser', 'replaceuser', 'replaceparty'):
        return ReturnValue({'errcode': -10003, 'errmsg': 
            'method should be syncuser, replaceuser, replaceparty'})
    data = {'media_id': csvMediaId,
        'callback': {
            'url': callbackUrl,
            'token': '__server.config.token',
            'encodingaeskey': '__server.config.encodingAesKey', }}
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    @access_token
    def upload(method, accessToken=None):
        url = '%s/cgi-bin/batch/%s?access_token=%s' % \
            (COMPANY_URL, method, accessToken)
        r = requests.post(url, data=data).json()
        return ReturnValue(r)
    return upload(method)

@access_token
def get_result(jobId, accessToken=None):
    params = {
        'access_token': accessToken,
        'jobid': jobId, }
    r = requests.get('%s/cgi-bin/batch/getresult' % COMPANY_URL,
        params=params).json()
    return ReturnValue(r)
