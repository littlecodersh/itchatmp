from .common import BaseController
from .mpapi.mp import utils as mpUtils

class Utils(BaseController):
    def create_qrcode(self, sceneData, expire=2592000):
        return self.determine_wrapper(mpUtils.create_qrcode, None,
            sceneData, expire)
    def download_qrcode(self, ticket):
        return self.determine_wrapper(mpUtils.download_qrcode, None,
            ticket)
    def long_url_to_short(self, url):
        return self.determine_wrapper(mpUtils.long_url_to_short, None,
            url)
