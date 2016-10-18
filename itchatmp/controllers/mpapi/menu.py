from .common import determine_wrapper as dwp
from .mp import menu as mpMenu

def create(menuDict, autoDecide=True):
    return dwp(mpMenu.create, None,
        menuDict, autoDecide)

def get():
    return dwp(mpMenu.get, None)

def delete():
    return dwp(mpMenu.delete, None)

def addconditional(menuDict, autoDecide=True):
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
