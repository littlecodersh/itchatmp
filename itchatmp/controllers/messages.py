from itchatmp.server import WechatServer
from .common import determine_wrapper
from .mpapi.mp import messages as mpMsg
from .mpapi.qy import messages as qyMsg

server = WechatServer(None, None, None)

def send_some(msgType, mediaId, additionalDict={},
        targetIdList=[], partyIdList=[], tagIdList=[],
        agentId=None):
    return determine_wrapper(mpMsg.send_some, qyMsg.send_some,
        msgType, mediaId, additionalDict,
        targetIdList, partyIdList, tagIdList, agentId)

def send_all(msgType, mediaId, additionalDict={},
        tagId=None, agentId=None):
    return determine_wrapper(mpMsg.send_all, qyMsg.send_all,
        msgType, mediaId, additionalDict, tagId, agentId)

def preview(msgType, mediaId, additionalDict={}, toUserId=None, toWxAccount=None):
    return determine_wrapper(mpMsg.preview, None,
        msgType, mediaId, additionalDict, toUserId, toWxAccount)

def delete(msgId):
    return determine_wrapper(mpMsg.delete, None,
        msgId)

def get(msgId):
    return determine_wrapper(mpMsg.get, None,
        msgId)

def upload(fileType, fileDir, additionalDict={}, permanent=False):
    return determine_wrapper(mpMsg.upload, qyMsg.upload,
        fileType, fileDir, additionalDict, permanent)

def download(mediaId):
    return determine_wrapper(mpMsg.download, qyMsg.download,
        mediaId)

def get_material(mediaId):
    return determine_wrapper(mpMsg.get_material, qyMsg.get_material,
        mediaId)

def delete_material(mediaId):
    return determine_wrapper(mpMsg.delete_material, qyMsg.delete_material,
        mediaId)

def get_materialcount():
    return determine_wrapper(mpMsg.get_materialcount, qyMsg.get_materialcount)

def batchget_material(fileType, offset=0, count=20):
    return determine_wrapper(mpMsg.batchget_material, qyMsg.batchget_material,
        fileType, offset, count)

def create_news(newsDict, permanent=False):
    return determine_wrapper(mpMsg.create_news, qyMsg.create_news,
        newsDict, permanent)

def update_news(mediaId, newsDict, index=0):
    return determine_wrapper(mpMsg.update_news, qyMsg.update_news,
        mediaId, newsDict, index)

def get_image_url(openedFile):
    return determine_wrapper(mpMsg.get_image_url, qyMsg.get_image_url,
        openedFile)

server.upload = upload
