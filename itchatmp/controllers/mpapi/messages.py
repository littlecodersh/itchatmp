import logging, json

from .requests import requests
from .common import access_token
from itchatmp.utils import retry, encode_send_dict
from itchatmp.content import SERVER_URL
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')
IMAGE, VOICE, VIDEO, THUMB = 'image', 'voice', 'video', 'thumb'

@retry(n=3, waitTime=3)
@access_token
def upload(fileDict, perment=False, accessToken=None):
    '''
     * fileDict should be like:
         {'file': file, 'type': type, 'details': {}}
    '''
    if not all([k in fileDict for k in ('file', 'type')]) or \
            (fileDict['type'] == VIDEO and not 'details' in fileDict):
        return ReturnValue({'errcode': -10001, 'errmsg': upload.__doc__})
    if not fileDict['type'] in (IMAGE, VOICE, VIDEO, THUMB):
        return ReturnValue({'errcode': 40004,})
    if perment:
        url = '%s/cgi-bin/material/add_material?access_token=%s&type=%s'
    else:
        url = '%s/cgi-bin/media/upload?access_token=%s&type=%s' 
    try:
        r = requests.post(url % (SERVER_URL, accessToken, t), files={'file': f},
            data=encode_send_dict(fileDict.get('details'))
            if fileDict['type'] == VIDEO else None).json()
        if 'media_id' in r: r['errcode'] = 0
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def download(mediaId, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/media/get?access_token=%s&media_id=%s' % 
            (SERVER_URL, accessToken, mediaId))
        if 'application/json' in r.headers['Content-Type']:
            return ReturnValue(r.json())
        else:
            tempStorage = io.BytesIO()
            for block in r.iter_content(1024):
                tempStorage.write(block)
            return ReturnValue({'file': tempStorage, 'errcode': 0})
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def upload_image(f, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/media/uploadimg?access_token=%s' % 
            (SERVER_URL, accessToken), files={'file': f}).json()
        if 'url' in r: r['errcode'] = 0
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def upload_video(videoDict, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/media/uploadvideo?access_token=%s' % 
            (SERVER_URL, accessToken), data=encode_send_dict(videoDict)).json()
        if 'media_id' in r: r['errcode'] = 0
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def upload_news(newsDict, perment=False, accessToken=None):
    if perment:
        url = '%s/cgi-bin/material/add_news?access_token=%s'
    else:
        url = '%s/cgi-bin/media/uploadnews?access_token=%s'
    try:
        r = requests.post(url % (SERVER_URL, accessToken),
            data=encode_send_dict(newsDict)).json()
        if 'media_id' in r: r['errcode'] = 0
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def send_all(msgDict, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/message/mass/sendall?access_token=%s' % 
            (SERVER_URL, accessToken), data=encode_send_dict(msgDict)).json()
        if 'media_id' in r: r['errcode'] = 0
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def send_one(msgDict, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/message/mass/send?access_token=%s' % 
            (SERVER_URL, accessToken), data=encode_send_dict(msgDict)).json()
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def delete(msgId, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/message/mass/delete?access_token=%s' % 
            (SERVER_URL, accessToken), data={'msg_id': msgId}).json()
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def preview(msgDict, toUserId=None, toWxAccount=None, accessToken=None):
    try:
        if (toUserId or toWxAccount) is None:
            raise Exception('toUserId or toWxAccount should be set')
        else:
            if toUserId is not None: msgDict['touser'] = toUserId
            if toWxAccount is not None: msgDict['towxname'] = toWxAccount
        r = requests.post('%s/cgi-bin/message/mass/preview?access_token=%s' % 
            (SERVER_URL, accessToken), data=encode_send_dict(msgDict)).json()
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def get(msgId, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/message/mass/get?access_token=%s' % 
            (SERVER_URL, accessToken), data={'msg_id': msgId}).json()
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def get_material(msgId, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/material/get_material?access_token=%s' % 
            (SERVER_URL, accessToken), data={'msg_id': msgId}).json()
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def delete_material(msgId, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/material/del_material?access_token=%s' % 
            (SERVER_URL, accessToken), data={'msg_id': msgId}).json()
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def update_news(newsDict, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/material/add_news?access_token=%s' %
            (SERVER_URL, accessToken), data=encode_send_dict(newsDict)).json()
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def get_materialcount(msgId, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/material/get_materialcount?access_token=%s'
            % (SERVER_URL, accessToken)).json()
        if 'voice_count' in r: r['errcode'] = 0
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def batchget_material(t, offset=0, count=20, accessToken=None):
    if not t in (IMAGE, VOICE, VIDEO, THUMB):
        return ReturnValue({'errcode': 40004,})
    if 20 < count: count = 20
    try:
        r = requests.post('%s/cgi-bin/material/batchget_material?access_token=%s'
            % (SERVER_URL, accessToken)).json()
        if 'total_count' in r: r['errcode'] = 0
        return ReturnValue(r)
    except Exception as e:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})
