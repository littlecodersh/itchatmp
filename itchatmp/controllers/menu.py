from .common import BaseController
from .mpapi.mp import menu as mpMenu
from .mpapi.qy import menu as qyMenu

class Menu(BaseController):
    def create(self, menuDict, agentId=None):
        return self.determine_wrapper(mpMenu.create, qyMenu.create,
            menuDict, agentId)
    def get(self, agentId=None):
        return self.determine_wrapper(mpMenu.get, qyMenu.get,
            agentId)
    def delete(self, agentId=None):
        return self.determine_wrapper(mpMenu.delete, qyMenu.delete,
            agentId)
    def addconditional(self, menuDict):
        return self.determine_wrapper(mpMenu.addconditional, None,
            menuDict)
    def delconditional(self, menuId):
        return self.determine_wrapper(mpMenu.delconditional, None,
            menuId)
    def trymatch(self, userId):
        return self.determine_wrapper(mpMenu.trymatch, None,
            userId)
    def get_current_selfmenu_info(self):
        return self.determine_wrapper(mpMenu.get_current_selfmenu_info, None)
