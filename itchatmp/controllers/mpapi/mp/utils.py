import logging, io

from tornado import gen
from ..requests import requests
from itchatmp.utils import retry, encode_send_dict
from itchatmp.config import SERVER_URL, COROUTINE
from itchatmp.returnvalues import ReturnValue

logger = logging.getLogger('itchatmp')

def create_qrcode(sceneData, expire=2592000, accessToken=None):
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
        if not 0 < expire < 2592000:
            expire = 2592000
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

    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/qrcode/create?access_token=%s'
        % (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        result = ReturnValue(result.json())
        if 'ticket' in result:
            result['errcode'] = 0
        return result
    r._wrap_result = _wrap_result
    return r

def download_qrcode(ticket):
    if COROUTINE:
        @gen.coroutine
        def _download_qrcode(ticket):
            params = {'ticket': ticket}
            r = yield requests.get('https://mp.weixin.qq.com/cgi-bin/showqrcode',
                params=params, stream=True)
            if 'application/json' in r.headers['Content-Type']:
                r = ReturnValue(r.json())
            else:
                tempStorage = io.BytesIO()
                for block in r.iter_content(1024):
                    tempStorage.write(block)
                r = ReturnValue({'File': tempStorage, 'errcode': 0})
            raise gen.Return(r)
    else:
        def _download_qrcode(ticket):
            params = {'ticket': ticket}
            r = requests.get('https://mp.weixin.qq.com/cgi-bin/showqrcode',
                params=params, stream=True)
            if 'application/json' in r.headers['Content-Type']:
                r = ReturnValue(r.json())
            else:
                tempStorage = io.BytesIO()
                for block in r.iter_content(1024):
                    tempStorage.write(block)
                r = ReturnValue({'File': tempStorage, 'errcode': 0})
            return r
    return _download_qrcode()

def long_url_to_short(url, accessToken=None):
    data = {'action': 'long2short', 'long_url': url}
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/shorturl?access_token=%s'
        % (SERVER_URL, accessToken), data=data)
    def _wrap_result(result):
        return ReturnValue(result.json())
    r._wrap_result = _wrap_result
    return r
