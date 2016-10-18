from .common import determine_wrapper
from .mp import messages as mpMsg

def send_some(msgType, mediaId, additionalDict={}, targetIdList=[]):
    return determine_wrapper(mpMsg.send_some, None,
        msgTyp, mediaId, additionalDict, targetIdList)

def send_all(msgType, mediaId, additionalDict={}, tagId=None):
    return determine_wrapper(mpMsg.send_all, None,
        msgType, mediaId, additionalDict, tagId)

def preview(msgType, mediaId, additionalDict={}, toUserId=None, toWxAccount=None):
    return determine_wrapper(mpMsg.preview, None,
        msgType, mediaId, additionalDict, toUserId, toWxAccount)

def delete(msgId):
    return determine_wrapper(mpMsg.delete, None,
        msgId)

def get(msgId):
    return determine_wrapper(mpMsg.get, None,
        msgId)

def upload(fileType, openedFile, additionalDict={}, perment=False):
    return determine_wrapper(mpMsg.get, None,
        fileType, openedFile, additionalDict, perment)

def download(mediaId):
    return determine_wrapper(mpMsg.download, None,
        mediaId)

def get_material(mediaId):
    return determine_wrapper(mpMsg.get_material, None,
        mediaId)

def delete_material(mediaId):
    return determine_wrapper(mpMsg.delete_material, None,
        mediaId)

def get_materialcount(mediaId):
    return determine_wrapper(mpMsg.get_materialcount, None,
        mediaId)

def batchget_material(fileType, offset=0, count=20):
    return determine_wrapper(mpMsg.batchget_material, None,
        fileType, offset, count)

def create_news(newsDict, perment=False):
    return determine_wrapper(mpMsg.create_news, None,
        newsDict, perment)

def update_news(newsDict):
    return determine_wrapper(mpMsg.update_news, None,
        newsDict)

def get_image_url(openedFile):
    return determine_wrapper(mpMsg.get_image_url, None,
        openedFile)
