from .common import BaseController
from .mpapi.mp import users as mpUsers
from .mpapi.qy import users as qyUsers

class Users(BaseController):
    def create_tag(self, name, id_=None):
        return self.determine_wrapper(mpUsers.create_tag, qyUsers.create_tag,
            name, id_)
    def get_tags(self):
        return self.determine_wrapper(mpUsers.get_tags, qyUsers.get_tags)
    def update_tag(self, id_, name):
        return self.determine_wrapper(mpUsers.update_tag, qyUsers.update_tag,
            id_, name)
    def delete_tag(self, id_):
        return self.determine_wrapper(mpUsers.delete_tag, qyUsers.delete_tag,
            id_)
    def get_users_of_tag(self, id_, nextOpenId=''):
        return self.determine_wrapper(mpUsers.get_users_of_tag, qyUsers.get_users_of_tag,
            id_, nextOpenId)
    def add_users_into_tag(self, id_, userIdList=None, partyList=None):
        return self.determine_wrapper(
            mpUsers.add_users_into_tag, qyUsers.add_users_into_tag,
            id_, userIdList, partyList)
    def delete_users_of_tag(self, id_, userIdList=None, partyList=None):
        return self.determine_wrapper(
            mpUsers.delete_users_of_tag, qyUsers.delete_users_of_tag,
            id_, userIdList, partyList)
    def get_tags_of_user(self, userId):
        return self.determine_wrapper(mpUsers.get_tags_of_user, None,
            userId)
    def set_alias(self, userId, alias):
        return self.determine_wrapper(mpUsers.set_alias, None,
            userId, alias)
    def get_user_info(self, userId):
        return self.determine_wrapper(mpUsers.get_user_info, qyUsers.get_user_info,
            userId)
    def get_users(self, nextOpenId='', departmentId=None, fetchChild=False, status=4):
        return self.determine_wrapper(mpUsers.get_users, qyUsers.get_users,
            nextOpenId, departmentId, fetchChild, status)
    def get_detailed_users(self, nextOpenId='', departmentId=None,
            fetchChild=False, status=4):
        return self.determine_wrapper(None, qyUsers.get_detailed_users,
            nextOpenId, departmentId, fetchChild, status)
    def get_blacklist(self, beginOpenId=''):
        return self.determine_wrapper(mpUsers.create_tag, None,
            beginOpenId)
    def add_users_into_blacklist(self, userId):
        return self.determine_wrapper(mpUsers.add_users_into_blacklist, None,
            userId)
    def delete_users_of_blacklist(self, userId):
        return self.determine_wrapper(mpUsers.delete_users_of_blacklist, None,
            userId)
    def authorize_user(self, userId):
        return self.determine_wrapper(None, qyUsers.authorize_user,
            userId)
    def create_department(self, name, parentId=1, order=None, id_=None):
        return self.determine_wrapper(None, qyUsers.create_department,
            name, parentId, order, id_)
    def update_department(self, id_, name=None, parentId=None, order=None):
        return self.determine_wrapper(None, qyUsers.update_department,
            id_, name, parentId, order)
    def delete_department(self, id_):
        return self.determine_wrapper(None, qyUsers.delete_department,
            id_)
    def get_departments(self, parentId):
        return self.determine_wrapper(None, qyUsers.get_departments,
            parentId)
    def create_user(self, userId, name, departmentIdList,
            position=None, mobile=None, gender=None, email=None,
            weixinId=None, headImgId=None, extAttr=None):
        return self.determine_wrapper(None, qyUsers.create_user,
            userId, name, departmentIdList, position,
            mobile, gender, email, weixinId, headImgId, extAttr)
    def update_user(self, userId, name=None, departmentIdList=None,
            position=None, mobile=None, gender=None, email=None,
            weixinId=None, headImgId=None, extAttr=None):
        return self.determine_wrapper(None, qyUsers.update_user,
            userId, name, departmentIdList, position,
            mobile, gender, email, weixinId, headImgId, extAttr)
    def delete_users(self, userId):
        return self.determine_wrapper(None, qyUsers.delete_users,
            userId)
    def upload_contract(self, csvMediaId, callbackUrl, method='sync'):
        return self.determine_wrapper(None, qyUsers.upload_contract,
            csvMediaId, callbackUrl, method)
    def get_result(self, jobId):
        return self.determine_wrapper(None, qyUsers.get_result,
            jobId)
