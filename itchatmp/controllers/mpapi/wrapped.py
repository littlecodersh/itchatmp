from itchatmp.server import WechatServer
from .common import determine_wrapper as dwp
from .mp import wrapped as mpWrapped

__server = WechatServer.instance()

def send(msg, toUserId):
    return dwp(mpWrapped.send, None,
        msg, toUserId)

__server._cssend = send
