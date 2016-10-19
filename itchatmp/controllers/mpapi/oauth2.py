from .common import determine_wrapper as dwp
from .qy import oauth2 as qyOauth

def generate_code_url(redirectUri, state=None):
    return dwp(None, qyOauth.generate_code_url,
        redirectUri, state)

def get_user_info(code, accessToken=None):
    return dwp(None, qyOauth.get_user_info,
        code)

def user_id_open_id_switch(userId=None, openId=None, agentId=None):
    return dwp(None, qyOauth.user_id_open_id_switch,
        userId, openId, agentId)
