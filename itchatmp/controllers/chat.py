from .common import BaseController
from .mpapi.qy import chat as qyChat

class Chat(BaseController):
    def send_some(self, msgType, mediaId, additionalDict={},
            targetIdList=[], partyIdList=[], tagIdList=[],
            agentId=None):
        return self.determine_wrapper(mpMsg.send_some, qyMsg.send_some,
            msgTyp, mediaId, additionalDict,
            targetIdList, partyIdList, tagIdList, agentId)
    def create(self, chatId, name, ownerId, userIdList):
        return self.determine_wrapper(None, qyChat.create,
            chatId, name, ownerId, userIdList)
    def get(self, chatId):
        return self.determine_wrapper(None, qyChat.get,
            chatId)
    def update(self, chatId, opUserId, name=None, ownerId=None,
            addUserIdList=None, delUserIdList=None):
        return self.determine_wrapper(None, qyChat.update,
            chatId, opUserId, name, ownerId, addUserIdList, delUserIdList)
    def quit(self, chatId, opUserId):
        return self.determine_wrapper(None, qyChat.quit,
            opUserId)
    def clear_notify(self, ownerId, chatId=None, userId=None):
        return self.determine_wrapper(None, qyChat.clear_notify,
            ownerId, chatId, userId)
    def send(self, msgType, mediaId, additionalDict={}, senderId=None,
            userId=None, chatId=None):
        return self.determine_wrapper(None, qyChat.send,
            msgTyp, mediaId, additionalDict, senderId, userId, chatId)
    def set_mute(self, muteList=[], cancelList=[]):
        return self.determine_wrapper(None, qyChat.set_mute,
            muteList, cancelList)
