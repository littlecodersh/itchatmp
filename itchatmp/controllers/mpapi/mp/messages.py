''' This package is for mass texting in wechat mp
 1. What can we send?
    - IMAGE, VOICE, VIDEO, TEXT, NEWS, CARD

 2. How to send them?
    - we use send_some / send_all method
        `send_some(targetIdList, msgType, mediaId, additionalDict)`
    - for msg like text and card, just pass content as msgId
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
     preview
   - MSG MANAGING
     delete
     get
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
import logging, json, os, mimetypes, io, re

from ..requests import requests
from itchatmp.utils import retry, encode_send_dict
from itchatmp.config import SERVER_URL
from itchatmp.content import (
    IMAGE, VOICE, VIDEO, THUMB, TEXT, NEWS, CARD)
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

def send_some(msgType, mediaId, additionalDict={},
        targetIdList=[], partyIdList=[], tagIdList=[],
        agentId=None, accessToken=None):
    msgDict = __form_send_dict(msgType, mediaId, additionalDict)
    if not msgDict: return msgDict
    if not isinstance(targetIdList, list) or len(targetIdList) < 2:
        return ReturnValue({'errcode': 40130})
    msgDict['touser'] = targetIdList
    r = requests.post('%s/cgi-bin/message/mass/send?access_token=%s' % 
        (SERVER_URL, accessToken), data=encode_send_dict(msgDict))
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def send_all(msgType, mediaId, additionalDict={},
        tagId=None, agentId=None, accessToken=None):
    msgDict = __form_send_dict(msgType, mediaId, additionalDict)
    if not msgDict: return msgDict
    if tagId is None: 
        msgDict['filter'] = {'is_to_all': True, 'tag_id': 0}
    else:
        msgDict['filter'] = {'is_to_all': False, 'tag_id': tagId}
    r = requests.post('%s/cgi-bin/message/mass/sendall?access_token=%s' % 
        (SERVER_URL, accessToken), data=encode_send_dict(msgDict))
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'media_id' in result: result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r

def preview(msgType, mediaId, additionalDict={},
        toUserId=None, toWxAccount=None, accessToken=None):
    msgDict = __form_send_dict(msgType, mediaId, additionalDict)
    if not msgDict: return msgDict
    if (toUserId or toWxAccount) is None:
        return ReturnValue({'errcode': -10003})
    else:
        if toUserId is not None: msgDict['touser'] = toUserId
        if toWxAccount is not None: msgDict['towxname'] = toWxAccount
    r = requests.post('%s/cgi-bin/message/mass/preview?access_token=%s' % 
        (SERVER_URL, accessToken), data=encode_send_dict(msgDict))
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def form_video_id(mediaId, additionalDict, accessToken=None):
    ''' in theory video needs another method to get media_id for sending '''
    additionalDict['media_id'] = mediaId
    additionalDict['description'] = additionalDict['introduction']
    # requests.packages.urllib3.disable_warnings()
    url = 'https://file.api.weixin.qq.com/cgi-bin/media/uploadvideo' \
        '?access_token=%s' % accessToken
    r = requests.post(url, data=encode_send_dict(additionalDict))
        # verify=False).json()
    # I don't know why this is a fake ssl
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'media_id' in result:
            result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r

def __form_send_dict(msgType, mediaId, additionalDict):
    if not msgType in (IMAGE, VOICE, VIDEO, TEXT, NEWS, CARD):
        return ReturnValue({'errcode': 40004,})
    elif msgType == VIDEO:
        mediaId = form_video_id(mediaId, additionalDict)['media_id']
        if not mediaId: return mediaId
    return {
        NEWS: {'mpnews':{'media_id': mediaId}, 'msgtype': 'mpnews'},
        TEXT: {'text': {'content': mediaId}, 'msgtype': 'text'},
        VOICE: {'voice': {'media_id': mediaId}, 'msgtype': 'voice'},
        IMAGE: {'image': {'media_id': mediaId}, 'msgtype': 'image'},
        VIDEO: {'mpvideo':{'media_id': mediaId,
            'title': additionalDict.get('title', ''),
            'description': additionalDict.get('introduction', '')},
            'msgtype': 'mpvideo'},
        CARD: {'wxcard': {'card_id': mediaId}, 'msgtype': 'wxcard'},
        }[msgType]

def delete(msgId, accessToken=None):
    r = requests.post('%s/cgi-bin/message/mass/delete?access_token=%s' % 
        (SERVER_URL, accessToken), data={'msg_id': msgId})
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def get(msgId, accessToken=None):
    r = requests.post('%s/cgi-bin/message/mass/get?access_token=%s' % 
        (SERVER_URL, accessToken), data={'msg_id': int(msgId)})
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def upload(fileType, fileDir, additionalDict={}, permanent=False, accessToken=None):
    if additionalDict: # format additionalDict
        for key in ('description',):
            if key in additionalDict and isinstance(additionalDict[key], dict):
                for k, v in additionalDict[key].items():
                    if k not in additionalDict:
                        additionalDict[k] = v
        additionalDict = {k.lower().replace('_', ''): v
            for k, v in additionalDict.items()}
        if 'introduction' in additionalDict:
            additionalDict['description'] = additionalDict['introduction']
    if not fileType in (IMAGE, VOICE, VIDEO, THUMB):
        return ReturnValue({'errcode': 40004,})
    elif fileType == VIDEO and permanent and not ('title' in additionalDict
            and 'description' in additionalDict):
        return ReturnValue({'errcode': -10003, 'errmsg':
            'additionalDict for type VIDEO should be: ' +
            "{'Title' : 'title', 'Description' :'des'}"})
    try:
        with open(fileDir, 'rb') as f:
            file_ = f.read()
    except:
        return ReturnValue({'errcode': -10004,})
    fileName = 'file' + os.path.splitext(fileDir)[1]
    if hasattr(fileName, 'decode'):
        fileName = fileName.decode('utf8', 'replace')
    fileMime = mimetypes.guess_type(fileName)[0] or 'application/octet-stream'
    if permanent:
        url = '%s/cgi-bin/material/add_material?access_token=%s&type=%s'
    else:
        url = '%s/cgi-bin/media/upload?access_token=%s&type=%s' 
    files = {'media': (fileName, file_, fileMime), }
    if fileType == VIDEO and permanent:
        files['description'] = (None, encode_send_dict({
            'title': additionalDict['title'],
            'introduction': additionalDict['description'], }
            ), 'application/json')
    r = requests.post(url % (SERVER_URL, accessToken, fileType),
        files=files)
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'media_id' in result:
            result['errcode'] = 0
        else:
            for k in result:
                if 'media_id' in k:
                    result['media_id'] = result[k]
                    result['errcode'] = 0
                    break
        return result
    r._wrap_result = _wrap_result
    return r

def download(mediaId, accessToken=None):
    r = requests.get('%s/cgi-bin/media/get?access_token=%s&media_id=%s' % 
        (SERVER_URL, accessToken, mediaId), stream=True)
    def _wrap_result(result):
        if 'text/plain' in result.headers['Content-Type']:
            j = result.json()
            if 'down_url' in j or 'news_item' in j:
                j['errcode'] = 0
            return ReturnValue(j)
        else:
            tempStorage = io.BytesIO()
            for block in result.iter_content(1024):
                tempStorage.write(block)
            basicDict = {'File': tempStorage, 'errcode': 0}
            if 'Content-disposition' in result.headers:
                match = re.search('filename="(.*?)"', result.headers['Content-disposition'])
                if match:
                    basicDict['FileName'] = match.group(1)
            if 'Content-Type' in result.headers:
                basicDict['ContentType'] = result.headers['Content-Type']
            if 'Content-Length' in result.headers:
                basicDict['ContentLength'] = result.headers['Content-Length']
            return ReturnValue(basicDict)
    r._wrap_result = _wrap_result
    return r

def get_material(mediaId, accessToken=None):
    data = {'media_id': mediaId}
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/material/get_material?access_token=%s' % 
        (SERVER_URL, accessToken), data=data, stream=True)
    def _wrap_result(result):
        if 'text/plain' in result.headers['Content-Type']:
            j = result.json()
            if 'down_url' in j or 'news_item' in j:
                j['errcode'] = 0
            return ReturnValue(j)
        else:
            tempStorage = io.BytesIO()
            for block in result.iter_content(1024):
                tempStorage.write(block)
            basicDict = {'File': tempStorage, 'errcode': 0}
            if 'Content-disposition' in result.headers:
                match = re.search('filename="(.*?)"', result.headers['Content-disposition'])
                if match:
                    basicDict['FileName'] = match.group(1)
            if 'Content-Type' in result.headers:
                basicDict['ContentType'] = result.headers['Content-Type']
            if 'Content-Length' in result.headers:
                basicDict['ContentLength'] = result.headers['Content-Length']
            return ReturnValue(basicDict)
    r._wrap_result = _wrap_result
    return r

def delete_material(mediaId, accessToken=None):
    r = requests.post('%s/cgi-bin/material/del_material?access_token=%s' % 
        (SERVER_URL, accessToken), data={'msg_id': mediaId})
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def get_material_count(accessToken=None):
    r = requests.get('%s/cgi-bin/material/get_materialcount?access_token=%s'
        % (SERVER_URL, accessToken))
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'voice_count' in result:
            result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r

def batchget_material(fileType, offset=0, count=20, accessToken=None):
    if not fileType in (IMAGE, VOICE, VIDEO, THUMB):
        return ReturnValue({'errcode': 40004,})
    if 20 < count: count = 20
    data = {'type': fileType,
        'offset': offset,
        'count': count, }
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/material/batchget_material?access_token=%s'
        % (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'total_count' in result: result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r

def create_news(newsDict, permanent=False, accessToken=None):
    if permanent:
        url = '%s/cgi-bin/material/add_news?access_token=%s'
    else:
        url = '%s/cgi-bin/media/uploadnews?access_token=%s'
    r = requests.post(url % (SERVER_URL, accessToken),
        data=encode_send_dict(newsDict))
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'media_id' in result: result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r

def update_news(mediaId, newsDict, index=0, accessToken=None):
    data = {
        'media_id': mediaId,
        'index': index,
        'articles': newsDict, }
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/material/update_news?access_token=%s' %
        (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def get_image_url(openedFile, accessToken=None):
    r = requests.post('%s/cgi-bin/media/uploadimg?access_token=%s' % 
        (SERVER_URL, accessToken), files={'file': openedFile})
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'url' in result: result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r

def get_autoreply(accessToken=None):
    r = requests.post('%s/cgi-bin/get_current_autoreply_info?access_token=%s' % 
        (SERVER_URL, accessToken))
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'is_autoreply_open' in result:
            result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r
