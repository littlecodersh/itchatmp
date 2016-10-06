import time
import lxml.etree as ET

from itchatmp.content import NEWS, MUSIC
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
    if replyDict['MsgType'] == NEWS:
        if not 0 < len(replyDict.get('Articles',{})) < 10:
            raise ItChatSDKException(
                'A news must have 1-9 articles')
        replyDict['ArticleCount'] = len(replyDict['Articles'])
        replyDict['Articles'] = ''.join(
            [_render(get_template('article'), msgDict, article)
            for article in replyDict['Articles']])
    elif replyDict['MsgType'] == MUSIC:
        template = get_template(MUSIC)
        if replyDict.get('ThumbMediaId') is None:
            template = template(1)
        else:
            template = template(0)
        return _render(template, msgDict, replyDict)
    return _render(get_template(replyDict['MsgType']), msgDict, replyDict)
