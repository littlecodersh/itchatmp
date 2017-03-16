from .common import BaseController
from .mpapi.mp import messages as mpMsg
from .mpapi.qy import messages as qyMsg

class Messages(BaseController):
    def send_some(self, msgType, mediaId, additionalDict={},
            targetIdList=[], partyIdList=[], tagIdList=[],
            agentId=None):
        return self.determine_wrapper(mpMsg.send_some, qyMsg.send_some,
            msgType, mediaId, additionalDict,
            targetIdList, partyIdList, tagIdList, agentId)
    def send_all(self, msgType, mediaId, additionalDict={},
            tagId=None, agentId=None):
        return self.determine_wrapper(mpMsg.send_all, qyMsg.send_all,
            msgType, mediaId, additionalDict, tagId, agentId)
    def preview(self, msgType, mediaId, additionalDict={}, toUserId=None, toWxAccount=None):
        return self.determine_wrapper(mpMsg.preview, None,
            msgType, mediaId, additionalDict, toUserId, toWxAccount)
    def delete(self, msgId):
        return self.determine_wrapper(mpMsg.delete, None,
            msgId)
    def get(self, msgId):
        return self.determine_wrapper(mpMsg.get, None,
            msgId)
    def upload(self, fileType, fileDir, additionalDict={}, permanent=False):
        return self.determine_wrapper(mpMsg.upload, qyMsg.upload,
            fileType, fileDir, additionalDict, permanent)
    def download(self, mediaId):
        return self.determine_wrapper(mpMsg.download, qyMsg.download,
            mediaId)
    def get_material(self, mediaId):
        return self.determine_wrapper(mpMsg.get_material, qyMsg.get_material,
            mediaId)
    def delete_material(self, mediaId):
        return self.determine_wrapper(mpMsg.delete_material, qyMsg.delete_material,
            mediaId)
    def get_material_count(self):
        return self.determine_wrapper(mpMsg.get_material_count, qyMsg.get_material_count)
    def batchget_material(self, fileType, offset=0, count=20):
        return self.determine_wrapper(mpMsg.batchget_material, qyMsg.batchget_material,
            fileType, offset, count)
    def create_news(self, newsDict, permanent=False):
        return self.determine_wrapper(mpMsg.create_news, qyMsg.create_news,
            newsDict, permanent)
    def update_news(self, mediaId, newsDict, index=0):
        return self.determine_wrapper(mpMsg.update_news, qyMsg.update_news,
            mediaId, newsDict, index)
    def get_image_url(self, openedFile):
        return self.determine_wrapper(mpMsg.get_image_url, qyMsg.get_image_url,
            openedFile)
    def get_autoreply(self):
        return self.determine_wrapper(mpMsg.get_autoreply, None)
