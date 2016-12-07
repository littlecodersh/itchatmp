from .common import determine_wrapper as dwp
from .mpapi.mp import templatemsgs as mpTMsg

def set_industry(id1, id2):
    return dwp(mpTMsg.set_industry, None,
        id1, id2)

def get_industry():
    return dwp(mpTMsg.get_industry, None)

def add_template(templateId):
    return dwp(mpTMsg.add_template, None,
        templateId)

def delete_templates(templateId):
    return dwp(mpTMsg.delete_templates, None,
        templateId)

def get_templates():
    return dwp(mpTMsg.get_templates, None)

def send(templateId, msgDict, toUserId):
    return dwp(mpTMsg.send, None,
        templateId, msgDict, toUserId)
