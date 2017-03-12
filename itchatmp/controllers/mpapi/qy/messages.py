''' This package is for mass texting in wechat company platform
 1. What can we send?
    - TEXT, IMAGE, VOICE, VIDEO, FILE, NEWS

 2. How to send them?
    - we use send_some / send_all method
        `send_some(targetIdList, msgType, mediaId, additionalDict
            targetIdList, partyIdList, tagIdList, agentId)`
    - for msg like text, just pass content as msgId
    - for files like image, voice, video, we need to upload them first
        `upload(fileType, openedFile, additionalDict, permanent)`
    - for news, you need to form them first and upload to get msgId
        `create_news(newsDict, permanent)`
      for images used in news, you need to turn them into url first
        `get_image_url(openedFile)`
    - SPECIAL WARNING: video is a little bit **STRANGE**
      when uploading or sending, you need to pass additionalDict to method
        `{"title" :VIDEO_TITLE, "introduction" :INTRODUCTION}`

 3. I alse listed API list for you:
   - SENDING
     send_some
     send_all
   - TEMP MATERIAL MANAGING
     upload
     download
   - PERMENENT MATERIAL MANAGING
     get_material
     delete_material
     get_materialcount
     batchget_material
   - FORM NEWS
     create_news
     update_news
     get_image_url
'''
import logging, json

from ..requests import requests
from .common import access_token
from itchatmp.utils import retry, encode_send_dict
from itchatmp.config import COMPANY_URL
from itchatmp.content import (FILE,
    IMAGE, VOICE, VIDEO, THUMB, TEXT, NEWS, CARD)
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

@access_token
def send_some(msgType, mediaId, additionalDict={},
        targetIdList=[], partyIdList=[], tagIdList=[],
        agentId=None, accessToken=None):
    msgDict = __form_send_dict(msgType, mediaId, additionalDict)
    if not msgDict:
        return msgDict
    elif not (targetIdList or partyIdList or tagIdList):
        return ReturnValue({'errcode': 40130, 'errmsg':
            'there must be one filled list'})
    elif agentId is None: 
        return ReturnValue({'errcode': -10003, 'errmsg':
            'agentId must be set'})
    msgDict['touser']  = '|'.join(targetIdList)
    msgDict['toparty'] = '|'.join(partyIdList)
    msgDict['totag']   = '|'.join(tagIdList)
    msgDict['agentid'] = agentId
    msgDict['safe']    = 0
    data = encode_send_dict(msgDict)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/message/send?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def send_all(msgType, mediaId, additionalDict={}, tagId=None,
        agentId=None, accessToken=None):
    msgDict = __form_send_dict(msgType, mediaId, additionalDict)
    if not msgDict:
        return msgDict
    elif agentId is None: 
        return ReturnValue({'errcode': -10003, 'errmsg':
            'agentId must be set'})
    msgDict['touser']  = '@all'
    msgDict['toparty'] = '@all'
    msgDict['totag']   = '@all'
    msgDict['agentid'] = agentId
    msgDict['safe']    = 0
    data = encode_send_dict(msgDict)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/message/send?access_token=%s' % 
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
        FILE: {'file': {'media_id': mediaId}, 'msgtype': 'file'},
        NEWS: {'mpnews':{'media_id': mediaId}, 'msgtype': 'mpnews'},
        }[msgType]

@access_token
def upload(fileType, fileDir, additionalDict={}, permanent=False, accessToken=None):
    if not fileType in (IMAGE, VOICE, VIDEO, FILE):
        return ReturnValue({'errcode': 40004,})
    # elif fileType == VIDEO and not ('title' in additionalDict
    #         and 'introduction' in additionalDict):
    #     return ReturnValue({'errcode': -10001, 'errmsg': 
    #         'additionalDict for type VIDEO should be: ' + 
    #         '{"title" :VIDEO_TITLE, "introduction" :INTRODUCTION}'})
    if permanent:
        url = '%s/cgi-bin/material/add_material?access_token=%s&type=%s'
    else:
        url = '%s/cgi-bin/media/upload?access_token=%s&type=%s' 
    # if fileType == VIDEO:
    #     files = {
    #         'description': (None, encode_send_dict(additionalDict),
    #             'application/json'),
    #         'file': ('tmp.mp4', openedFile, 'video/mp4') }
    # else:
    if hasattr(fileDir, 'fileno'):
        files = {'file': fileDir}
        r = requests.post(url % (COMPANY_URL, accessToken, fileType),
            files=files).json()
    else:
        with open(fileDir, 'rb') as f:
            files = {'file': f}
            r = requests.post(url % (COMPANY_URL, accessToken, fileType),
                files=files).json()
    if 'media_id' in r:
        r['errcode'] = 0
    return ReturnValue(r)

@access_token
def download(mediaId, accessToken=None):
    params = {
        'access_token': accessToken,
        'media_id': mediaId, }
    r = requests.get('%s/cgi-bin/media/get' % COMPANY_URL, stream=True)
    if 'application/json' in r.headers['Content-Type']:
        return ReturnValue(r.json())
    else:
        tempStorage = io.BytesIO()
        for block in r.iter_content(1024):
            tempStorage.write(block)
        return ReturnValue({'file': tempStorage, 'errcode': 0})

@access_token
def get_material(mediaId, accessToken=None):
    params = {
        'media_id': mediaId,
        'access_token': accessToken, }
    r = requests.get('%s/cgi-bin/material/get' % COMPANY_URL,
        params=params, stream=True)
    if 'application/json' in r.headers['Content-Type']:
        j = r.json()
        if 'type' in j: j['errcode'] = 0
        return ReturnValue(j)
    else:
        tempStorage = io.BytesIO()
        for block in r.iter_content(1024):
            tempStorage.write(block)
        return ReturnValue({'file': tempStorage, 'errcode': 0})
    return ReturnValue(r)

@access_token
def delete_material(mediaId, accessToken=None):
    params = {
        'media_id': mediaId,
        'access_token': accessToken, }
    r = requests.get('%s/cgi-bin/material/del' % COMPANY_URL,
        params=params).json()
    return ReturnValue(r)

@access_token
def get_material_count(accessToken=None):
    r = requests.get('%s/cgi-bin/material/get_count?access_token=%s'
        % (COMPANY_URL, accessToken)).json()
    return ReturnValue(r)

@access_token
def batchget_material(fileType, offset=0, count=20, accessToken=None):
    if not fileType in (NEWS, IMAGE, VOICE, VIDEO, FILE):
        return ReturnValue({'errcode': 40004,})
    if fileType == NEWS: fileType = 'mpnews'
    if 50 < count: count = 50
    data = {'type': fileType,
        'offset': offset,
        'count': count, }
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/material/batchget?access_token=%s'
        % (COMPANY_URL, accessToken), data=data).json()
    if 'itemlist' in r: r['errcode'] = 0
    return ReturnValue(r)

@access_token
def create_news(newsDict, permanent=False, accessToken=None):
    if permanent:
        url = '%s/cgi-bin/material/add_mpnews?access_token=%s'
    else:
        return ReturnValue({'errcode': -10003, 'errmsg':
            'All news must be permanent for company platform'})
    data = encode_send_dict(newsDict)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post(url % (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def update_news(mediaId, newsDict, index=0, accessToken=None):
    data = {
        'media_id': mediaId,
        'mpnews': newsDict, }
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/material/update_mpnews?access_token=%s' %
        (COMPANY_URL, accessToken), data=data).json()
    return ReturnValue(r)

@access_token
def get_image_url(openedFile, accessToken=None):
    r = requests.post('%s/cgi-bin/media/uploadimg?access_token=%s' % 
        (COMPANY_URL, accessToken), files={'file': openedFile}).json()
    if 'url' in r: r['errcode'] = 0
    return ReturnValue(r)
