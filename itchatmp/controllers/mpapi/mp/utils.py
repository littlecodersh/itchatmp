import logging, io

from ..requests import requests
from .common import access_token
from itchatmp.utils import retry, encode_send_dict
from itchatmp.content import SERVER_URL
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

def create_qrcode(sceneData, expire=2592000):
    ''' create qrcode with specific data
     * qrcode can be permanent, if so you need to set expire to False
     * sceneData can be string or integer if it's permanent
     * but it can only be integer if it's not
    '''
    data = {'action_info': {'scene': {}}}

    try:
        expire = int(expire)
    except ValueError:
        return ReturnValue({'errcode': -10003, 'errmsg': 'expire should be int'})
    if not (isinstance(sceneData, int) or hasattr(sceneData, 'capitalize')):
        return ReturnValue({'errcode': -10003, 'errmsg':
            'sceneData should be int or string'})

    if expire:
        if not isinstance(sceneData, int):
            return ReturnValue({'errcode': -10003, 'errmsg':
                'sceneData for tmp qrcode can only be int'})
        if not 0 < expire < 2592000: expire = 2592000
        data['expire_seconds'] = expire
        data['action_name'] = 'QR_SCENE'
        data['action_info']['scene']['scene_id'] = sceneData
    else:
        if isinstance(sceneData, int):
            data['action_name'] = 'QR_LIMIT_SCENE'
            data['action_info']['scene']['scene_id'] = sceneData
        else:
            data['action_name'] = 'QR_LIMIT_STR_SCENE'
            data['action_info']['scene']['scene_str'] = sceneData

    @retry(n=3, waitTime=3)
    @access_token
    def _create_qrcode(data, accessToken=None):
        data = encode_send_dict(data)
        if data is None: return ReturnValue({'errcode': -10001})
        r = requests.post('%s/cgi-bin/qrcode/create?access_token=%s'
            % (SERVER_URL, accessToken), data=data).json()
        if 'ticket' in r: r['errcode'] = 0
        return ReturnValue(r)
    return _create_qrcode(data)

@retry(n=3, waitTime=3)
def download_qrcode(ticket):
    params = {'ticket': ticket}
    r = requests.get('https://mp.weixin.qq.com/cgi-bin/showqrcode',
        params=params, stream=True)
    if 'application/json' in r.headers['Content-Type']:
        return ReturnValue(r.json())
    else:
        tempStorage = io.BytesIO()
        for block in r.iter_content(1024):
            tempStorage.write(block)
        return ReturnValue({'file': tempStorage, 'errcode': 0})

@retry(n=3, waitTime=3)
@access_token
def long_url_to_short(url, accessToken=None):
    data = {'action': 'long2short', 'long_url': url}
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/shorturl?access_token=%s'
        % (SERVER_URL, accessToken), data=data).json()
    return ReturnValue(r)
