from itchatmp.config import COMPANY_URL
from itchatmp.returnvalues import ReturnValue
from itchatmp.utils import retry, encode_send_dict
from ..requests import requests
from .common import access_token

@access_token
def get(agentId, accessToken=None):
    params = {
        'access_token': accessToken,
        'agentid': agentId, }
    r = requests.get('%s/cgi-bin/agent/get' % COMPANY_URL,
        params=params).json()
    return ReturnValue(r)

@access_token
def set(agentId, **kwargs):
    kwargs['agentid'] = agentId
    data = encode_send_dict(kwargs)
    if data is None: return ReturnValue({'errcode': -10001})
    r = requests.post('%s/cgi-bin/agent/set?access_token=%s' %
        (COMPANY_URL, kwargs['accessToken']), data=data).json()
    return ReturnValue(r)

@access_token
def list(accessToken=None):
    r = requests.get('%s/cgi-bin/agent/list?access_token=%s' % \
        (COMPANY_URL, accessToken)).json()
    return ReturnValue(r)
