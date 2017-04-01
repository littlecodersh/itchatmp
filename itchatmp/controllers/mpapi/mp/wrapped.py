import re, logging

from tornado import gen

from itchatmp.config import COROUTINE
from itchatmp.content import (MUSIC,
    IMAGE, VOICE, VIDEO, THUMB, TEXT, NEWS, CARD)
from itchatmp.returnvalues import ReturnValue
from itchatmp.views import reply_msg_format

logger = logging.getLogger('itchatmp')

def send(core, msg, toUserId, mediaId=None, accessToken=None):
    ''' This is a method for sending messages to a specific user
     1. How this works?
        - if the user has contacted mp in 48 hours, use customerservice.send
        - if not, use messages.preview
        - MUSIC, which doesn't support preview will return 45015 (out of 48h)
     2. What should be passed into msg
        - it can be a string (for encoding other than ascii, unicode should be used)
          - it should start with things like @img@
          - then it should follow mediaId or fileDir (for text, it's content)
          - it supports: img, voc, vid, txt, nws, cad (msc is not supported)
        - it can be a dict (for encoding other than ascii, unicode should be used)
          - value of key "MsgType" should be the msgType
          - value of key "MediaId" should be mediaId (for text, value is content)
          - for VIDEO, there need to be two more keys:
            - Title, Introduction
          - for MUSIC, there need to be three more keys:
            - MusicUrl, HqMusicUrl, ThumbMediaId
          - it supports all types: img, voc, vid, txt, nws, cad, msc
    '''
    msg = reply_msg_format(msg) # format string into dict
    # filter unexpected messages
    if 'MsgType' in msg:
        msgType = msg['MsgType']
    else:
        return ReturnValue({'errcode': -10003, 'errmsg': 
            'value of key "MsgType" should be a valid message type'})
    if msgType not in (IMAGE, VOICE, VIDEO, TEXT, NEWS, CARD, MUSIC):
        return ReturnValue({'errcode': -10003, 'errmsg': 
            'send supports: IMAGE, VOICE, VIDEO, TEXT, NEWS, CARD, MUSIC'})
    if COROUTINE:
        @gen.coroutine
        def _send(mediaId):
            mediaId = mediaId or msg.get('MediaId', '')
            if 'FileDir' in msg and msgType != TEXT and not mediaId:
                r = yield core.messages.upload(msgType, msg['FileDir'], msg, msg.get('Permanent', False))
                if not r:
                    raise gen.Return(r)
                mediaId = r['media_id']
            r = yield core.customerservice.send(msgType, mediaId, additionalDict=msg, toUserId=toUserId)
            r['preview'] = False
            if not r:
                if r['errcode'] != 45015 or msgType == MUSIC:
                    raise gen.Return(r)
                r = yield core.messages.preview(msgType, mediaId, additionalDict=msg, toUserId=toUserId)
                r['preview'] = True
            raise gen.Return(r)
        return _send(mediaId)
    else:
        mediaId = mediaId or msg.get('MediaId', '')
        if 'FileDir' in msg and msgType != TEXT and not mediaId:
            r = core.messages.upload(msgType, msg['FileDir'], msg, msg.get('Permanent', False))
            if not r:
                return r
            mediaId = r['media_id']
        r = core.customerservice.send(msgType, mediaId, additionalDict=msg, toUserId=toUserId)
        r['preview'] = False
        if not r:
            if r['errcode'] != 45015 or msgType == MUSIC:
                return r
            r = core.messages.preview(msgType, mediaId, additionalDict=msg, toUserId=toUserId)
            r['preview'] = True
        return r
