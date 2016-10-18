import functools

from .server import WechatConfig, WechatServer
from .models.common import TestStorage
from .controllers.envtest import env_test
from .controllers.mpapi import (common, menu,
    customerservice, messages, users, utils, statistics)
from .controllers.mpapi.wrapped import send

from .log import logger

__version__ = '0.0.2'

# env_test()

__server = WechatServer.instance()

update_config = __server.update_config
run = __server.run
msg_register = __server.msg_register
