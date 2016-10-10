import time, logging
import lxml.etree as ET

from itchatmp.content import VIDEO, MUSIC, NEWS, ENCRYPT
from itchatmp.exceptions import ParameterError
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
    except Exception as e:
        logger.debug(e.message)
    if r.get('Encrypt') is not None:
        r['MsgType'] = r.get('MsgType') or ENCRYPT
    return r

def construct_msg(msgDict, replyDict):
    ''' construct xml msg from dict to string
     * if deconstruct failed will return an empty string
    '''
    def _render(template, msgDict, replyDict):
        try:
            return template.format(
                ToUserName=msgDict['FromUserName'],
                FromUserName=msgDict['ToUserName'],
                CreateTime=int(time.time()),
                **replyDict)
        except KeyError as e:
            logger.debug('Missing message element "%s"' % e.message)
        except UnicodeDecodeError as e:
            logger.debug('All non-ascii values should be unicode like: u"value"')
        except:
            logger.debug(
                'Wrong format of reply message: ' + str(replyDict))
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
            [_render(get_template('article'), msgDict, article)
            for article in replyDict['Articles']])
    return _render(get_template(replyDict['MsgType']), msgDict, replyDict)
