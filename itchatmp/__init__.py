import functools

from .server import WechatConfig, WechatServer

__version__ = '0.0.0'

__server = WechatServer.instance()

update_config = __server.update_config
run = __server.run
msg_register = __server.msg_register
