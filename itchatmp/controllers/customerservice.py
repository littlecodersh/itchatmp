from .common import determine_wrapper as dwp
from .mpapi.mp import customerservice as mpCs

def get():
    return dwp(mpCs.get, None)

def add(accountDict, autoDecide=True):
    return dwp(mpCs.add, None,
        accountDict, autoDecide)

def update(accountDict, autoDecide=True):
    return dwp(mpCs.update, None,
        accountDict, autoDecide)

def delete(accountDict, autoDecide=True):
    return dwp(mpCs.delete, None,
        accountDict, autoDecide)

def set_head_image(openedFile, kfAccount):
    return dwp(mpCs.set_head_image, None,
        openedFile, kfAccount)

def send(msgType, mediaId, additionalDict={}, toUserId=''):
    return dwp(mpCs.send, None,
        msgType, mediaId, additionalDict, toUserId)
