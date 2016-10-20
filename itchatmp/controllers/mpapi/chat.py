from .common import determine_wrapper as dwp
from .qy import chat as qyChat

def send_some(msgType, mediaId, additionalDict={},
        targetIdList=[], partyIdList=[], tagIdList=[],
        agentId=None):
    return dwp(mpMsg.send_some, qyMsg.send_some,
        msgTyp, mediaId, additionalDict,
        targetIdList, partyIdList, tagIdList, agentId)

def create(chatId, name, ownerId, userIdList):
    return dwp(None, qyChat.create,
        chatId, name, ownerId, userIdList)

def get(chatId):
    return dwp(None, qyChat.get,
        chatId)

def update(chatId, opUserId, name=None, ownerId=None,
        addUserIdList=None, delUserIdList=None):
    return dwp(None, qyChat.update,
        chatId, opUserId, name, ownerId, addUserIdList, delUserIdList)

def quit(chatId, opUserId):
    return dwp(None, qyChat.quit,
        opUserId)

def clear_notify(ownerId, chatId=None, userId=None):
    return dwp(None, qyChat.clear_notify,
        ownerId, chatId, userId)

def send(msgType, mediaId, additionalDict={}, senderId=None,
        userId=None, chatId=None):
    return dwp(None, qyChat.send,
        msgTyp, mediaId, additionalDict, senderId, userId, chatId)

def set_mute(muteList=[], cancelList=[]):
    return dwp(None, qyChat.set_mute,
        muteList, cancelList)
