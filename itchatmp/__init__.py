from .server import WechatConfig, WechatServer
from .models.common import TestStorage
from .controllers.envtest import env_test
from .controllers.mpapi import (common, menu,
    customerservice, messages, users, utils, statistics,
    oauth2)

from .log import set_logging

__version__ = '0.0.4'

server = WechatServer(None, None, None)

update_config = server.update_config
run           = server.run
msg_register  = server.msg_register
send          = server.send
set_logging   = set_logging
