from itchatmp.returnvalues import ReturnValue

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
        pass
    elif isinstance(msg, dict): # msg is a dict
        pass
    else:
        return ReturnValue({'errcode': -10003,
            'errmsg': 'msg should be a string or dict'})
