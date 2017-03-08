import time, logging, re, os
import traceback
try:
    import lxml.etree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from itchatmp.content import (ENCRYPT, MUSIC,
    IMAGE, VOICE, VIDEO, THUMB, TEXT, NEWS, CARD)
from itchatmp.exceptions import ParameterError
from itchatmp.returnvalues import ReturnValue
from .templates import get_template

logger = logging.getLogger('itchatmp')

def deconstruct_msg(msg):
    ''' deconstruct xml msg from string to dict
     * use lxml to save time
     * if deconstruct failed will return an empty dict
    '''
    r = {}
    def _get_dict(msg, d):
        for i in msg:
            if i.text is None:
                d[i.tag] = {}
                _get_dict(i, d[i.tag])
            else:
                d[i.tag] = i.text
    try:
        _get_dict(ET.fromstring(msg), r)
    except:
        logger.debug(traceback.format_exc())
    if 'Encrypt' in r:
        r['MsgType'] = r.get('MsgType') or ENCRYPT
    return r

def reply_msg_format(msg):
    ''' turns string reply to reply dict
     * if format failed, it will return a ReturnValue equals to False
     * if succeeded, it will return a dict equals to string
    '''
    if isinstance(msg, dict):
        r = msg
    elif hasattr(msg, 'capitalize'):
        msgType, content = msg[:5], msg[5:]
        r = {}
        if not re.match('@[a-z]{3}@', msgType):
            r['MsgType'] = TEXT
            r['MediaId'] = msgType + content
        elif msgType[1:4] == 'msc':
            return ReturnValue({'errcode': -10003, 'errmsg': 
                'msg for type MUSIC should be: {"msgType": MUSIC, ' + 
                '"musicurl" :MUSICURL, "hqmusicurl" :HQMUSICURL, ' +
                '"thumb_media_id": MEDIA_ID}'})
        elif msgType[1:4] not in ('img', 'voc', 'vid', 'txt', 'nws', 'cad'):
            return ReturnValue({'errcode': -10003, 'errmsg': 
                'send supports: img, voc, vid, txt, nws, cad'})
        else:
            r['MsgType'] = {'img': IMAGE, 'voc': VOICE, 'vid': VIDEO, 'txt': TEXT,
                'nws': NEWS, 'cad': CARD}[msgType[1:4]]
            r['FileDir'] = content
    else:
        r = ReturnValue({'errcode': -10003, 'errmsg': 
            'msg should be string or dict'})
    if r and r.get('MsgType') == TEXT:
        if 'MediaId' not in r and 'Content' in r:
            r['MediaId'] = r['Content']
        elif 'MediaId' in r and 'Content' not in r:
            r['Content'] = r['MediaId']
    return r

def construct_msg(replyDict):
    ''' construct xml msg from dict to string
     * if deconstruct failed will return an empty string
    '''
    def _render(template, replyDict):
        try:
            if 'CreateTime' not in replyDict:
                replyDict['CreateTime'] = int(time.time())
            return template.format(**replyDict)
        except KeyError as e:
            logger.debug('Missing message element "%s"' % e.message)
        except UnicodeDecodeError as e:
            logger.debug('All non-ascii values should be unicode like: u"value"')
        except:
            logger.debug(
                'Wrong format of reply message: ' + str(replyDict))
            logger.debug(traceback.format_exc())
        return ''
    def _fill_key(d, k):
        d[k] = d.get(k, '')
    if replyDict['MsgType'] == VIDEO:
        for k in ('Title', 'Description'):
            _fill_key(replyDict, k)
    elif replyDict['MsgType'] == MUSIC:
        for k in ('Title', 'Description', 'MusicURL', 'HQMusicUrl'):
            _fill_key(replyDict, k)
    elif replyDict['MsgType'] == NEWS:
        for k in ('Title', 'Description', 'PicUrl', 'Url'):
            _fill_key(replyDict, k)
        if not 0 < len(replyDict.get('Articles',{})) < 10:
            raise ParameterError(
                'A news must have 1-9 articles')
        replyDict['ArticleCount'] = len(replyDict['Articles'])
        replyDict['Articles'] = ''.join(
            [_render(get_template('article'), article)
            for article in replyDict['Articles']])
    return _render(get_template(replyDict['MsgType']), replyDict)
