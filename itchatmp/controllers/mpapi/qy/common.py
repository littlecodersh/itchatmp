from requests import get

from itchatmp.config import COMPANY_URL, COROUTINE
from itchatmp.returnvalues import ReturnValue
from itchatmp.utils import retry
from ..requests import requests

update_access_token = access_token = get_server_ip = \
    filter_request = lambda x: x
