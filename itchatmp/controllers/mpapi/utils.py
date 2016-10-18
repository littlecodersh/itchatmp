from .common import determine_wrapper as dwp
from .mp import utils as mpUtils

def create_qrcode(sceneData, expire=2592000):
    return dwp(mpUtils.create_qrcode, None,
        sceneData, expire)

def download_qrcode(ticket):
    return dwp(mpUtils.download_qrcode, None,
        ticket)

def long_url_to_short(url):
    return dwp(mpUtils.long_url_to_short, None,
        url)
