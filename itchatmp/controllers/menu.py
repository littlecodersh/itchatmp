from .common import determine_wrapper as dwp
from .mpapi.mp import menu as mpMenu
from .mpapi.qy import menu as qyMenu

def create(menuDict, autoDecide=False, agentId=None):
    return dwp(mpMenu.create, qyMenu.create,
        menuDict, autoDecide, agentId)

def get(agentId=None):
    return dwp(mpMenu.get, qyMenu.get,
        agentId)

def delete(agentId=None):
    return dwp(mpMenu.delete, qyMenu.delete,
        agentId)

def addconditional(menuDict, autoDecide=False):
    return dwp(mpMenu.addconditional, None,
        menuDict, autoDecide)
    
def delconditional(menuId):
    return dwp(mpMenu.delconditional, None,
        menuId)

def trymatch(userId):
    return dwp(mpMenu.trymatch, None,
        userId)

def get_current_selfmenu_info():
    return dwp(mpMenu.get_current_selfmenu_info, None)
