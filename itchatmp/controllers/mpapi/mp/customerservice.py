import logging, json

from ..requests import requests
from itchatmp.utils import retry, encode_send_dict
from itchatmp.content import (
    IMAGE, VOICE, VIDEO, MUSIC, TEXT, NEWS, CARD)
from itchatmp.config import SERVER_URL, COROUTINE
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

def get(accessToken=None):
    r = requests.post('%s/cgi-bin/customservice/getkflist?access_token=%s'
        % (SERVER_URL, accessToken))
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'kf_list' in result: result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r

def add(accountDict, accessToken=None):
    data = encode_send_dict(accountDict)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/customservice/kfaccount/add?access_token=%s'
        % (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def update(accountDict, accessToken=None):
    data = encode_send_dict(accountDict)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/customservice/kfaccount/add?access_token=%s'
        % (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def delete(accountDict, accessToken=None):
    data = encode_send_dict(accountDict)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/customservice/kfaccount/del?access_token=%s'
        % (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def set_head_image(openedFile, kfAccount, accessToken=None):
    r = requests.post('%s/customservice/kfaccount/uploadheadimg?'
        'access_token=%s&kf_account=%s' % 
        (SERVER_URL, accessToken, kfAccount),
        files={'file': openedFile})
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def send(msgType, mediaId, additionalDict={}, toUserId='', accessToken=None):
    msgDict = __form_send_dict(msgType, mediaId, additionalDict)
    if not msgDict:
        return msgDict
    msgDict['touser'] = toUserId
    data = encode_send_dict(msgDict)
    if data is None:
        return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/message/custom/send?access_token=%s'
        % (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def __form_send_dict(msgType, mediaId, additionalDict):
    ''' additionalDict will be formatted to give full compacity to input
    thumb_media_id, ThumbMediaId, thumbmediaid are all supported '''
    if not msgType in (IMAGE, VOICE, VIDEO, TEXT, NEWS, CARD, MUSIC):
        return ReturnValue({'errcode': 40008,})
    if additionalDict: # format additionalDict
        for key in ('text', 'image', 'voice', 'video',
                'music', 'news', 'mpnews', 'wxcard'):
            if key in additionalDict and isinstance(additionalDict[key], dict):
                for k, v in additionalDict[key].items():
                    if k not in additionalDict:
                        additionalDict[k] = v
        additionalDict = {k.lower().replace('_', ''): v
            for k, v in additionalDict.items()}
        if 'cardid' in additionalDict:
            additionalDict['mediaid'] = additionalDict['cardid']
        if 'introduction' in additionalDict:
            additionalDict['description'] = additionalDict['introduction']
    if msgType == VIDEO:
        if not all((k in additionalDict for k in ('title', 'description'))):
            return ReturnValue({'errcode': -10003, 'errmsg': 
                'additionalDict for type VIDEO should be: ' + 
                "{'ThumbMediaId': 'id', 'Title': 'title', " +
                "'Description': 'des'}"})
    elif msgType == MUSIC:
        if not all((k in additionalDict for k in ('title', 'description',
                'musicurl', 'hqmusicurl', 'thumbmediaid'))):
            return ReturnValue({'errcode': -10003, 'errmsg': 
                'additionalDict for type MUSIC should be: ' + 
                "{'MusicUrl' : 'url', 'HqMusicUrl' : 'url', " +
                "'Title': 'title', 'Description': 'des', " +
                "'ThumbMediaId': 'id'}"})
    elif msgType == NEWS:
        if 'articles' not in additionalDict:
            msgType = 'mpnews'
    return {
        TEXT: {'text': {'content': mediaId}, 'msgtype': 'text'},
        IMAGE: {'image': {'media_id': mediaId}, 'msgtype': 'image'},
        VOICE: {'voice': {'media_id': mediaId}, 'msgtype': 'voice'},
        VIDEO: {'video': {'media_id': mediaId,
                'thumb_media_id': additionalDict.get('thumbmediaid', ''),
                'title': additionalDict.get('title', ''),
                'description': additionalDict.get('description', '')},
            'msgtype': 'video'},
        MUSIC: {'music': {
                'title': additionalDict.get('title', ''),
                'description': additionalDict.get('description', ''),
                'musicurl': additionalDict.get('musicurl', ''),
                'hqmusicurl': additionalDict.get('hqmusicurl', ''),
                'thumb_media_id': additionalDict.get('thumbmediaid', ''), },
            'msgtype': 'music'},
        NEWS: {'news':{'articles': additionalDict.get('articles', [])},
            'msgtype': 'news'},
        'mpnews': {'mpnews':{'media_id': mediaId}, 'msgtype': 'mpnews'},
        CARD: {'wxcard': {'card_id': mediaId}, 'msgtype': 'wxcard'},
        }[msgType]
