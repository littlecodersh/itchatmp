from .common import BaseController
from .mpapi.qy import oauth2 as qyOauth

class Oauth2(BaseController):
    def generate_code_url(self, redirectUri, state=None):
        return self.determine_wrapper(None, qyOauth.generate_code_url,
            redirectUri, state)
    def get_user_info(self, code, accessToken=None):
        return self.determine_wrapper(None, qyOauth.get_user_info,
            code)
    def user_id_open_id_switch(self, userId=None, openId=None, agentId=None):
        return self.determine_wrapper(None, qyOauth.user_id_open_id_switch,
            userId, openId, agentId)
