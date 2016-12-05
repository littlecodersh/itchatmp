from itchatmp.server import WechatServer
from .common import determine_wrapper as dwp
from .mp import wrapped as mpWrapped

server = WechatServer(None, None, None)

def send(msg, toUserId):
    return dwp(mpWrapped.send, None,
        msg, toUserId)

server.send = send
