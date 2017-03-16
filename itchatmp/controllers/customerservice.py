from .common import BaseController
from .mpapi.mp import customerservice as mpCs

class CustomerService(BaseController):
    def get(self):
        return self.determine_wrapper(mpCs.get, None)
    def add(self, accountDict, autoDecide=True):
        return self.determine_wrapper(mpCs.add, None,
            accountDict, autoDecide)
    def update(self, accountDict, autoDecide=True):
        return self.determine_wrapper(mpCs.update, None,
            accountDict, autoDecide)
    def delete(self, accountDict, autoDecide=True):
        return self.determine_wrapper(mpCs.delete, None,
            accountDict, autoDecide)
    def set_head_image(self, openedFile, kfAccount):
        return self.determine_wrapper(mpCs.set_head_image, None,
            openedFile, kfAccount)
    def send(self, msgType, mediaId, additionalDict={}, toUserId=''):
        return self.determine_wrapper(mpCs.send, None,
            msgType, mediaId, additionalDict, toUserId)
