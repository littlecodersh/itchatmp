import time
import lxml.etree as ET

from itchatmp.content import VIDEO, MUSIC, NEWS, ENCRYPT
from itchatmp.exceptions import ItChatSDKException
from .templates import get_template

def deconstruct_msg(msg):
    r = {}
    def _get_dict(msg, d):
        for i in msg:
            if i.text is None:
                d[i.tag] = {}
                _get_dict(i, d[i.tag])
            else:
                d[i.tag] = i.text
    _get_dict(ET.fromstring(msg), r)
    if r.get('Encrypt') is not None:
        r['MsgType'] = r.get('MsgType') or ENCRYPT
    return r

def construct_msg(msgDict, replyDict):
    def _render(template, msgDict, replyDict):
        try:
            return template.format(
                ToUserName=msgDict['FromUserName'],
                FromUserName=msgDict['ToUserName'],
                CreateTime=int(time.time()),
                **replyDict)
        except KeyError as e:
            raise ItChatSDKException(
                'Missing message element "%s"' % e.message)
        except:
            raise ItChatSDKException(
                'Wrong format of reply message: ' + str(replyDict))
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
            raise ItChatSDKException(
                'A news must have 1-9 articles')
        replyDict['ArticleCount'] = len(replyDict['Articles'])
        replyDict['Articles'] = ''.join(
            [_render(get_template('article'), msgDict, article)
            for article in replyDict['Articles']])
    return _render(get_template(replyDict['MsgType']), msgDict, replyDict)
