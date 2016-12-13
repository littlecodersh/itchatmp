import logging, json

from ..requests import requests
from .common import access_token
from itchatmp.utils import retry, encode_send_dict
from itchatmp.content import (
    IMAGE, VOICE, VIDEO, MUSIC, TEXT, NEWS, CARD)
from itchatmp.config import SERVER_URL, COROUTINE
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

@access_token
def get(accessToken=None):
    r = requests.post('%s/cgi-bin/customservice/getkflist?access_token=%s'
        % (SERVER_URL, accessToken))
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'kf_list' in result: result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r

def add(accountDict, autoDecide=True):
    @access_token
    def _add(accountDict, accessToken):
        data = encode_send_dict(accountDict)
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/customservice/kfaccount/add?access_token=%s'
            % (SERVER_URL, accessToken), data=data)
        def _wrap_result(result):
            return ReturnValue(result.json())
        r._wrap_result = _wrap_result
        return r
    if autoDecide and not COROUTINE:
        currentList = get()
        for kf in currentList.get('kf_list', []):
            if kf['kf_account'] == accountDict.get('kf_account'):
                logger.debug('kf already exists')
                return ReturnValue({'errcode': 0})
    return _add(accountDict)

def update(accountDict, autoDecide=True):
    @access_token
    def _update(accountDict, accessToken):
        data = encode_send_dict(accountDict)
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/customservice/kfaccount/add?access_token=%s'
            % (SERVER_URL, accessToken), data=data)
        def _wrap_result(result):
            return ReturnValue(result.json())
        r._wrap_result = _wrap_result
        return r
    if autoDecide and COROUTINE:
        currentList = get()
        for kf in currentList.get('kf_list', []):
            if kf['kf_account'] == accountDict.get('kf_account'):
                if kf['nickname'] == accountDict.get('nickname') and \
                        kf['password'] == accountDict.get('password'):
                    logger.debug('kf already have specific info')
                    break
        else:
            return ReturnValue({'errcode': 61452})
    return _update(accountDict)

def delete(accountDict, autoDecide=True):
    @access_token
    def _delete(accountDict, accessToken):
        data = encode_send_dict(accountDict)
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/customservice/kfaccount/del?access_token=%s'
            % (SERVER_URL, accessToken), data=data)
        def _wrap_result(result):
            return ReturnValue(result.json())
        r._wrap_result = _wrap_result
        return r
    if autoDecide and COROUTINE:
        currentList = get()
        for kf in currentList.get('kf_list', []):
            if kf['kf_account'] == accountDict.get('kf_account'):
                return _delete(accountDict)
    else:
        return _delete(accountDict)
    return ReturnValue({'errcode': 61452})

@access_token
def set_head_image(openedFile, kfAccount, accessToken=None):
    r = requests.post('%s/customservice/kfaccount/uploadheadimg?'
        'access_token=%s&kf_account=%s' % 
        (SERVER_URL, accessToken, kfAccount),
        files={'file': openedFile})
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

@access_token
def send(msgType, mediaId, additionalDict={}, toUserId='', accessToken=None):
    msgDict = __form_send_dict(msgType, mediaId, additionalDict)
    if not msgDict: return msgDict
    msgDict['touser'] = toUserId
    data = encode_send_dict(msgDict)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/message/custom/send?access_token=%s'
        % (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r

def __form_send_dict(msgType, mediaId, additionalDict):
    if not msgType in (IMAGE, VOICE, VIDEO, TEXT, NEWS, CARD, MUSIC):
        return ReturnValue({'errcode': 40008,})
    elif msgType == MUSIC:
        if not ('musicurl' in additionalDict and 'hqmusicurl' in additionalDict
                and 'thumb_media_id' in additionalDict):
            return ReturnValue({'errcode': -10003, 'errmsg': 
                'additionalDict for type VIDEO should be: ' + 
                '{"musicurl" :MUSICURL, "hqmusicurl" :HQMUSICURL, ' +
                '"thumb_media_id": MEDIA_ID}'})
    elif msgType == NEWS:
        if 'articles' in additionalDict:
            msgType = 'mpnews'
    return {
        TEXT: {'text': {'content': mediaId}, 'msgtype': 'text'},
        IMAGE: {'image': {'media_id': mediaId}, 'msgtype': 'image'},
        VOICE: {'voice': {'media_id': mediaId}, 'msgtype': 'voice'},
        VIDEO: {'video': {'media_id': mediaId,
            'thumb_media_id': additionalDict.get('thumb_media_id', ''),
            'title': additionalDict.get('title', ''),
            'description': additionalDict.get('introduction', '')},
            'msgtype': 'video'},
        MUSIC: {'music': {
            'thumb_media_id': additionalDict.get('thumb_media_id', ''),
            'title': additionalDict.get('title', ''),
            'description': additionalDict.get('description', ''),
            'musicurl': additionalDict.get('musicurl', ''),
            'hqmusicurl': additionalDict.get('hqmusicurl', '')},
            'msgtype': 'music'},
        NEWS: {'news':{'articles': additionalDict.get('articles', [])},
            'msgtype': 'mpnews'},
        'mpnews': {'mpnews':{'media_id': mediaId}, 'msgtype': 'mpnews'},
        CARD: {'wxcard': {'card_id': mediaId}, 'msgtype': 'wxcard'},
        }[msgType]
