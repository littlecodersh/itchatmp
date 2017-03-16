from .common import BaseController
from .mpapi.qy import application as qyApp

class Application(BaseController):
    def get(self, agentId):
        return self.determine_wrapper(None, qyApp.get,
            agentId)
    def set(self, agentId, **kwargs):
        return self.determine_wrapper(None, qyApp.set,
            agentId, **kwargs)
    def list(self):
        return self.determine_wrapper(None, qyApp.list)
