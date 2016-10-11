import logging, json

from .requests import requests
from .common import access_token
from itchatmp.utils import retry, encode_send_dict
from itchatmp.content import SERVER_URL
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

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
def upload_news(newsDict, accessToken=None):
    try:
        r = requests.post('%s/cgi-bin/media/uploadnews?access_token=%s' % 
            (SERVER_URL, accessToken), data=encode_send_dict(newsDict)).json()
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
