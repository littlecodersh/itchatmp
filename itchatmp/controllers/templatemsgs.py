from .common import BaseController
from .mpapi.mp import templatemsgs as mpTMsg

class TemplateMsgs(BaseController):
    def set_industry(self, id1, id2):
        return self.determine_wrapper(mpTMsg.set_industry, None,
            id1, id2)
    def get_industry(self):
        return self.determine_wrapper(mpTMsg.get_industry, None)
    def add_template(self, templateId):
        return self.determine_wrapper(mpTMsg.add_template, None,
            templateId)
    def delete_templates(self, templateId):
        return self.determine_wrapper(mpTMsg.delete_templates, None,
            templateId)
    def get_templates(self):
        return self.determine_wrapper(mpTMsg.get_templates, None)
    def send(self, templateId, msgDict, toUserId):
        return self.determine_wrapper(mpTMsg.send, None,
            templateId, msgDict, toUserId)
