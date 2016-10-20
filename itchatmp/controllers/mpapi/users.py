from .common import determine_wrapper as dwp
from .mp import users as mpUsers
from .qy import users as qyUsers

def create_tag(name, id=None):
    return dwp(mpUsers.create_tag, qyUsers.create_tag,
        name, id)

def get_tags():
    return dwp(mpUsers.get_tags, qyUsers.get_tags)

def update_tag(id, name):
    return dwp(mpUsers.update_tag, qyUsers.update_tag,
        id, name)

def delete_tag(id):
    return dwp(mpUsers.delete_tag, qyUsers.delete_tag,
        id)

def get_users_of_tag(id, nextOpenId=''):
    return dwp(mpUsers.get_users_of_tag, qyUsers.get_users_of_tag,
        id, nextOpenId)

def add_users_into_tag(id, userIdList=None, partyList=None):
    return dwp(mpUsers.add_users_into_tag, qyUsers.add_users_into_tag,
        id, userIdList, partyList)

def delete_users_of_tag(id, userIdList=None, partyList=None):
    return dwp(mpUsers.delete_users_of_tag, qyUsers.delete_users_of_tag,
        id, userIdList, partyList)

def get_tags_of_user(userId):
    return dwp(mpUsers.get_tags_of_user, None,
        userId)

def set_alias(userId, alias):
    return dwp(mpUsers.set_alias, None,
        userId, alias)

def get_user_info(userId):
    return dwp(mpUsers.get_user_info, qyUsers.get_user_info,
        userId)

def get_users(nextOpenId='', departmentId=None, fetchChild=False, status=4):
    return dwp(mpUsers.get_users, qyUsers.get_users,
        nextOpenId, departmentId, fetchChild, status)

def get_detailed_users(nextOpenId='', departmentId=None, fetchChild=False, status=4):
    return dwp(None, qyUsers.get_detailed_users,
        nextOpenId, departmentId, fetchChild, status)

def get_blacklist(beginOpenId=''):
    return dwp(mpUsers.create_tag, None,
        beginOpenId)

def add_users_into_blacklist(userId):
    return dwp(mpUsers.add_users_into_blacklist, None,
        userId)

def delete_users_of_blacklist(userId):
    return dwp(mpUsers.delete_users_of_blacklist, None,
        userId)

def authorize_user(userId):
    return dwp(None, qyUsers.authorize_user,
        userId)

def create_department(name, parentId=1, order=None, id=None):
    return dwp(None, qyUsers.create_department,
        name, parentId, order, id)

def update_department(id, name=None, parentId=None, order=None):
    return dwp(None, qyUsers.update_department,
        id, name, parentId, order)

def delete_department(id):
    return dwp(None, qyUsers.delete_department,
        id)

def get_departments(parentId):
    return dwp(None, qyUsers.get_departments,
        parentId)

def create_user(userId, name, departmentIdList,
        position=None, mobile=None, gender=None, email=None,
        weixinId=None, headImgId=None, extAttr=None):
    return dwp(None, qyUsers.create_user,
        userId, name, departmentIdList, position,
        mobile, gender, email, weixinId, headImgId, extAttr)

def update_user(userId, name=None, departmentIdList=None,
        position=None, mobile=None, gender=None, email=None,
        weixinId=None, headImgId=None, extAttr=None):
    return dwp(None, qyUsers.update_user,
        userId, name, departmentIdList, position,
        mobile, gender, email, weixinId, headImgId, extAttr)

def delete_users(userId):
    return dwp(None, qyUsers.delete_users,
        userId)

def upload_contract(csvMediaId, callbackUrl, method='sync'):
    return dwp(None, qyUsers.upload_contract,
        csvMediaId, callbackUrl, method)

def get_result(jobId):
    return dwp(None, qyUsers.get_result,
        jobId)
