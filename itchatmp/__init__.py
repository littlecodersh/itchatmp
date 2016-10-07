import functools

from .server import WechatConfig, WechatServer
from .controllers.envtest import env_test

__version__ = '0.0.0'

env_test()

__server = WechatServer.instance()

update_config = __server.update_config
run = __server.run
msg_register = __server.msg_register
