import re, logging

from tornado import gen

from itchatmp.config import COROUTINE
from itchatmp.content import (MUSIC,
    IMAGE, VOICE, VIDEO, THUMB, TEXT, NEWS, CARD)
from itchatmp.returnvalues import ReturnValue
from itchatmp.views import reply_msg_format
from .customerservice import send as cssend
from .messages import preview, upload

logger = logging.getLogger('itchatmp')

def send(msg, toUserId, mediaId=None):
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
          - for MUSIC, there need to be three more keys:
            - musicurl, hqmusicurl, thumb_media_id
          - it supports all types: img, voc, vid, txt, nws, cad, msc
    '''
    msg = reply_msg_format(msg) # format string into dict
    # get msgType and mediaId
    if not ('MsgType' in msg and 'MediaId' in msg):
        return ReturnValue({'errcode': -10003, 'errmsg': 
            'value of key "MsgType" should be the msgType and ' +
            'value of key "MediaId" should be mediaId (for text, value is content)'
            })
    else:
        msgType, content = msg['MsgType'], msg['MediaId']
    # filter unexpected messages
    if msgType not in (IMAGE, VOICE, VIDEO, TEXT, NEWS, CARD, MUSIC):
        return ReturnValue({'errcode': -10003, 'errmsg': 
            'send supports: IMAGE, VOICE, VIDEO, TEXT, NEWS, CARD, MUSIC'})
    elif msgType == MUSIC and not ('musicurl' in msg and 'hqmusicurl' in msg):
        return ReturnValue({'errcode': -10003, 'errmsg': 
            'msg for type MUSIC should be: {"msgType": MUSIC, ' + 
            '"musicurl" :MUSICURL, "hqmusicurl" :HQMUSICURL, ' +
            '"thumb_media_id": MEDIA_ID}'})
    if COROUTINE:
        @gen.coroutine
        def _send():
            # deal with mediaId and fileDir
            if mediaId is not None and msgType != TEXT:
                c = mediaId
            elif 'FileDir' in msg:
                r = yield upload(msgType, msg['FileDir'])
                if not r: raise gen.Return(r)
                c = r['media_id']
            else:
                c = content
            r = yield cssend(msgType, c, additionalDict=msg, toUserId=toUserId)
            r['preview'] = False
            if not r:
                if r['errcode'] != 45015 or msgType == MUSIC: raise gen.Return(r)
                r = yield preview(msgType, content, additionalDict=msg, toUserId=toUserId)
                r['preview'] = True
            raise gen.Return(r)
        return _send()
    else:
        # deal with mediaId and fileDir
        if mediaId is not None and msgType != TEXT:
            content = mediaId
        elif 'FileDir' in msg:
            r = upload(msgType, msg['FileDir'])
            if not r: return r
            content = r['media_id']
        r = cssend(msgType, content, additionalDict=msg, toUserId=toUserId)
        r['preview'] = False
        if not r:
            if r['errcode'] != 45015 or msgType == MUSIC: return r
            r = preview(msgType, content, additionalDict=msg, toUserId=toUserId)
            r['preview'] = True
        return r
