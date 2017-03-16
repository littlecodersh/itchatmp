from .common import BaseController
from .mpapi.mp import wrapped as mpWrapped

class Wrapped(BaseController):
    def send(self, msg, toUserName, mediaId=None):
        return self.determine_wrapper(mpWrapped.send, None,
            msg, toUserName, mediaId)
