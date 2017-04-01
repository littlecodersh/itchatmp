try:
    from urllib import quote_plus as quote
except ImportError:
    from urllib.parse import quote_plus as quote
import time
from itchatmp.config import COMPANY_URL
from itchatmp.returnvalues import ReturnValue
from itchatmp.utils import retry, encode_send_dict
from ..requests import requests
from .common import access_token

# __server
def generate_code_url(redirectUri, state=None):
    ''' generate redirect url for visiting with code
     * you don't need to urlencode redirectUri
    '''
    return ('https://open.weixin.qq.com/connect/oauth2/authorize?' + 
        'appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base' +
        '&state=%s#wechat_redirect') % \
        ('__server.config.copId', quote(redirectUri), quote((state or str(int(time.time())))))

@access_token
def get_user_info(code, accessToken=None):
    params = {
        'access_token': accessToken,
        'code': code, }
    r = requests.get('%s/cgi-bin/user/getuserinfo' % COMPANY_URL,
        params=params).json()
    if 'DeviceId' in r: r['errcode'] = 0
    return ReturnValue(r)

@access_token
def user_id_open_id_switch(userId=None, openId=None, agentId=None, accessToken=None):
    data = {}
    if userId:
        data['userid'] = userId
        if agentId: data['agentid'] = agentId
        url = '%s/cgi-bin/user/convert_to_openid?access_token=' + accessToken
    elif openId:
        data['openid'] = openId
        url = '%s/cgi-bin/user/convert_to_userid?access_token=' + accessToken
    data = encode_send_dict(data)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post(url % COMPANY_URL, data=data).json()
    return ReturnValue(r)

@access_token
def get_login_info(code, accessToken=None):
    data = {'auth_code': code, }
    r = requests.post('%s/cgi-bin/service/get_login_info?access_token=%s' % 
        (COMPANY_URL, accessToken), data=data).json()
    if 'usertype' in r: r['errcode'] = 0
    return ReturnValue(r)
