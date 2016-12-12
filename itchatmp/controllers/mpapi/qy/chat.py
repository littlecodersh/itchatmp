import logging

from ..requests import requests
from .common import access_token
from itchatmp.utils import retry, encode_send_dict
from itchatmp.config import COMPANY_URL
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

@access_token
def create(chatId, name, ownerId, userIdList, accessToken=None):
    if ownerId not in userIdList:
        return ReturnValue({'errcode': -10003, 'errmsg':
            'owner should be in userIdList'})
    data = {
        'chatid': chatId,
        'name': name,
        'owner': ownerId,
        'userlist': userIdList, }
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/chat/create?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def get(chatId, accessToken=None):
    params = {
        'chatid': chatId,
        'access_token': accessToken, }
    r = requests.get('%s/cgi-bin/chat/get' % COMPANY_URL,
        params=params).json()
    return ReturnValue(r)

@access_token
def update(chatId, opUserId, name=None, ownerId=None,
        addUserIdList=None, delUserIdList=None, accessToken=None):
    data = {
        'chatid': chatId,
        'op_user': opUserId,
        'name': name,
        'owner': ownerId,
        'add_user_list': addUserIdList,
        'del_user_list': delUserIdList, }
    for k in list(data):
        if data[k] is None: del data[k]
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/chat/update?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def quit(chatId, opUserId, accessToken=None):
    data = {
        'chatid': chatId,
        'op_user': opUserId, }
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/chat/quit?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def clear_notify(ownerId, chatId=None, userId=None, accessToken=None):
    data = {
        'op_user': ownerId,
        'chat': {
            'type': 'group' if chatId else 'single',
            'id': chatId or userId, }}
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/chat/clearnotify?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def send(msgType, mediaId, additionalDict={}, senderId=None,
        userId=None, chatId=None, accessToken=None):
    msgDict = __form_send_dict(msgType, mediaId, additionalDict)
    if not msgDict: return msgDict
    msgDict['receiver'] = {
        'type': 'single' if userId else 'group',
        'id': userId or chatId, }
    msgDict['sender'] = senderId
    data = encode_send_dict(msgDict)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/chat/send?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

def __form_send_dict(msgType, mediaId, additionalDict):
    if not msgType in (TEXT, IMAGE, VOICE, VIDEO, FILE, NEWS):
        return ReturnValue({'errcode': 40004,})
    return {
        TEXT: {'text': {'content': mediaId}, 'msgtype': 'text'},
        IMAGE: {'image': {'media_id': mediaId}, 'msgtype': 'image'},
        VOICE: {'voice': {'media_id': mediaId}, 'msgtype': 'voice'},
        VIDEO: {'video':{'media_id': mediaId,
            'title': additionalDict.get('title', ''),
            'description': additionalDict.get('introduction', '')},
            'msgtype': 'video'},
        FILE: {'media_id': mediaId, 'msgtype': 'file'},
        NEWS: {'mpnews':{'media_id': mediaId}, 'msgtype': 'mpnews'},
        }[msgType]

@access_token
def set_mute(muteList=[], cancelList=[], accessToken=None):
    l = []
    for status, userIdList in enumerate((cancelList, muteList)):
        for userId in userIdList:
            l.append({'userid': userId,
                'status': status, })
    data = {'user_mute_list': l}
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/chat/setmute?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)
