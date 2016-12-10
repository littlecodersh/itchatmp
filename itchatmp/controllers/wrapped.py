from itchatmp.server import WechatServer
from .common import determine_wrapper as dwp
from .mpapi.mp import wrapped as mpWrapped

server = WechatServer(None, None, None)

def send(msg, toUserName, mediaId=None):
    return dwp(mpWrapped.send, None,
        msg, toUserName, mediaId)

server.send = send
