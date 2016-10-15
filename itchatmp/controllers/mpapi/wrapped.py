import re, logging

from itchatmp.returnvalues import ReturnValue
from itchatmp.content import (MUSIC,
    IMAGE, VOICE, VIDEO, THUMB, TEXT, NEWS, CARD)
from .customerservice import send as cssend
from .messages import preview

logger = logging.getLogger('itchatmp')

def send(msg, toUserId):
    ''' This is a method for sending messages to a specific user
     1. How this works?
        - if the user has contacted mp in 48 hours, use customerservice.send
        - if not, use messages.preview
        - MUSIC, which doesn't support preview will return 45015 (out of 48h)
     2. What should be passed into msg
        - it can be a string (for encoding other than ascii, unicode should be used)
          - it should start with things like @img@
          - then it should follow mediaId (for text, it's content)
          - it supports: img, voc, vid, txt, nws, cad (msc is not supported)
        - it can be a dict (for encoding other than ascii, unicode should be used)
          - value of key "msgType" should be the msgType
          - value of key "mediaId" should be mediaId (for text, value is content)
          - for MUSIC, there need to be three more keys:
            - musicurl, hqmusicurl, thumb_media_id
          - it supports all types: img, voc, vid, txt, nws, cad, msc
    '''
    if hasattr(msg, 'capitalize'): # msg is a string
        msgType, content = msg[:5], msg[5:]
        if not re.match('@[a-z]{3}@', msgType):
            content = msgType + content
            msgType = TEXT
        elif msgType[1:4] == 'msc':
            return ReturnValue({'errcode': -10003, 'errmsg': 
                'msg for type MUSIC should be: {"msgType": MUSIC, ' + 
                '"musicurl" :MUSICURL, "hqmusicurl" :HQMUSICURL, ' +
                '"thumb_media_id": MEDIA_ID}'})
        elif msgType[1:4] not in ('img', 'voc', 'vid', 'txt', 'nws', 'cad'):
            return ReturnValue({'errcode': -10003, 'errmsg': 
                'send supports: img, voc, vid, txt, nws, cad'})
        else:
            msgType = {'img': IMAGE, 'voc': VOICE, 'vid': VIDEO, 'txt': TEXT,
                'nws': NEWS, 'cad': CARD}[msgType[1:4]]
        r = cssend(msgType, content, toUserId=toUserId)
        r['preview'] = False
        if not r:
            if r['errcode'] != 45015: return r
            r = preview(msgType, content, toUserId=toUserId)
            r['preview'] = True
        return r
    elif isinstance(msg, dict): # msg is a dict
        if not ('msgType' in msg and 'mediaId' in msg):
            return ReturnValue({'errcode': -10003, 'errmsg': 
                'value of key "msgType" should be the msgType and ' +
                'value of key "mediaId" should be mediaId (for text, value is content)'
                })
        else:
            msgType, content = msg['msgType'], msg['mediaId']
        if msgType not in (IMAGE, VOICE, VIDEO, TEXT, NEWS, CARD, MUSIC):
            return ReturnValue({'errcode': -10003, 'errmsg': 
                'send supports: IMAGE, VOICE, VIDEO, TEXT, NEWS, CARD, MUSIC'})
        elif msgType == MUSIC and not ('musicurl' in msg and 'hqmusicurl' in msg):
            return ReturnValue({'errcode': -10003, 'errmsg': 
                'msg for type MUSIC should be: {"msgType": MUSIC, ' + 
                '"musicurl" :MUSICURL, "hqmusicurl" :HQMUSICURL, ' +
                '"thumb_media_id": MEDIA_ID}'})
        r = cssend(msgType, content, additionalDict=msg, toUserId=toUserId)
        r['preview'] = False
        if not r:
            if r['errcode'] != 45015 or msgType == MUSIC: return r
            r = preview(msgType, content, additionalDict=msg, toUserId=toUserId)
            r['preview'] = True
        return r
    else:
        return ReturnValue({'errcode': -10003,
            'errmsg': 'msg should be a string or dict'})
