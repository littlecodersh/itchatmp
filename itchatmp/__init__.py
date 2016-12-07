from .server import WechatConfig, WechatServer
from .models.common import TestStorage
from .controllers.envtest import env_test
from .controllers import (
    application, chat, common, menu,
    customerservice, messages, users, utils, statistics,
    templatemsgs, oauth2, wrapped)

from .log import set_logging

__version__ = '0.0.4'

server = WechatServer(None, None, None)

update_config = server.update_config
run           = server.run
msg_register  = server.msg_register
send          = server.send
set_logging   = set_logging
