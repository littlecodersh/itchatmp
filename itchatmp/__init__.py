from .server import WechatConfig, WechatServer
from .models.common import TestStorage
from .config import VERSION
from .controllers.envtest import env_test

from .log import set_logging

__version__ = VERSION

instanceList = []

def new_instance():
    newInstance = WechatServer(None, None, None)
    instanceList.append(newInstance)
    return newInstance

originInstance = new_instance()

# I really want to use sys.modules[__name__] = originInstance
# but it makes auto-fill a real mess, so forgive me for my following **
# actually it toke me less than 30 seconds, god bless Uganda

set_logging   = set_logging

update_config = originInstance.update_config
run           = originInstance.run
msg_register  = originInstance.msg_register
send          = originInstance.send
access_token  = originInstance.access_token
clear_quota   = originInstance.clear_quota

application = originInstance.application
chat = originInstance.chat
common = originInstance.common
customerservice = originInstance.customerservice
menu = originInstance.menu
messages = originInstance.messages
oauth2 = originInstance.oauth2
statistics = originInstance.statistics
templatemsgs = originInstance.templatemsgs
users = originInstance.users
utils = originInstance.utils
wrapped = originInstance.wrapped
