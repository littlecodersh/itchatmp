import logging, json

from .requests import requests
from .common import access_token
from itchatmp.utils import retry, encode_send_dict
from itchatmp.content import SERVER_URL
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

@retry(n=3, waitTime=3)
@access_token
def get(accessToken=None):
    r = requests.post('%s/cgi-bin/customservice/getkflist?access_token=%s'
        % (SERVER_URL, accessToken)).json()
    if 'kf_list' in r: r['errcode'] = 0
    return ReturnValue(r)

def add(accountDict, autoDecide=True):
    @retry(n=3, waitTime=3)
    @access_token
    def _add(accountDict, accessToken):
        data = encode_send_dict(accountDict)
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/customservice/kfaccount/add?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        return ReturnValue(r)
    if autoDecide:
        currentList = get()
        for kf in currentList.get('kf_list', []):
            if kf['kf_account'] == accountDict.get('kf_account'):
                logger.debug('kf already exists')
                return ReturnValue({'errcode': 0})
    return _add(accountDict)

def update(accountDict, autoDecide=True):
    @retry(n=3, waitTime=3)
    @access_token
    def _update(accountDict, accessToken):
        data = encode_send_dict(accountDict)
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/customservice/kfaccount/add?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        return ReturnValue(r)
    if autoDecide:
        currentList = get()
        for kf in currentList.get('kf_list', []):
            if kf['kf_account'] == accountDict.get('kf_account'):
                if kf['nickname'] == accountDict.get('nickname') and \
                        kf['password'] == accountDict.get('password'):
                    logger.debug('kf already have specific info')
                    break
        else:
            return ReturnValue({'errcode': 61452})
    return _update(accountDict)

def delete(accountDict, autoDecide=True):
    @retry(n=3, waitTime=3)
    @access_token
    def _delete(accountDict, accessToken):
        data = encode_send_dict(accountDict)
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/customservice/kfaccount/del?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        return ReturnValue(r)
    if autoDecide:
        currentList = get()
        for kf in currentList.get('kf_list', []):
            if kf['kf_account'] == accountDict.get('kf_account'):
                return _delete(accountDict)
    else:
        return _delete(accountDict)
    return ReturnValue({'errcode': 61452})

@retry(n=3, waitTime=3)
@access_token
def set_head_image(f, kfAccount, accessToken=None):
    try:
        r = requests.post('%s/customservice/kfaccount/uploadheadimg?'
            'access_token=%s&kf_account=%s' % 
            (SERVER_URL, accessToken, kfAccount), files={'file': f}).json()
        return ReturnValue(r)
    except:
        return ReturnValue({'errcode': -10001, 'errmsg': e.message})

@retry(n=3, waitTime=3)
@access_token
def send(msgDict, accessToken=None):
    data = encode_send_dict(accountDict)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/message/custom/send?access_token=%s'
        % (SERVER_URL, accessToken), data=data).json()
    return ReturnValue(r)
