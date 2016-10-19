from .common import determine_wrapper as dwp
from .qy import application as qyApp

def get(agentId):
    return dwp(None, qyApp.get,
        agentId)

def set(agentId, **kwargs):
    return dwp(None, qyApp.set,
        agentId, **kwargs)

def list():
    return dwp(None, qyApp.list)
