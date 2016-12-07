from itchatmp.config import COMPANY_URL
from ..base.menu import create_producer, get_producer, delete_producer
from .common import access_token

create = create_producer(COMPANY_URL, access_token)

get = get_producer(COMPANY_URL, access_token)

delete = delete_producer(COMPANY_URL, access_token)
