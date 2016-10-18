from .common import determine_wrapper as dwp
from .mp import users as mpUsers

def create_tag(name):
    return dwp(mpUsers.create_tag, None,
        name)

def get_tags():
    return dwp(mpUsers.get_tags, None)

def update_tag(id, name):
    return dwp(mpUsers.update_tag, None,
        id, name)

def delete_tag(id):
    return dwp(mpUsers.delete_tag, None,
        id)

def get_users_of_tag(id, nextOpenId=''):
    return dwp(mpUsers.get_users_of_tag, None,
        id, nextOpenId)

def add_users_into_tag(id, userIdList):
    return dwp(mpUsers.add_users_into_tag, None,
        id, userIdList)

def delete_users_of_tag(id, userIdList):
    return dwp(mpUsers.delete_users_of_tag, None,
        id, userIdList)

def get_tags_of_user(userId):
    return dwp(mpUsers.get_tags_of_user, None,
        userId)

def set_alias(userId, alias):
    return dwp(mpUsers.set_alias, None,
        userId, alias)

def get_user_info(userId):
    return dwp(mpUsers.get_user_info, None,
        userId)

def get_users(nextOpenId=''):
    return dwp(mpUsers.get_users, None,
        nextOpenId)

def get_blacklist(beginOpenId=''):
    return dwp(mpUsers.create_tag, None,
        beginOpenId)

def add_users_into_blacklist(userId):
    return dwp(mpUsers.add_users_into_blacklist, None,
        userId)

def delete_users_of_blacklist(userId):
    return dwp(mpUsers.delete_users_of_blacklist, None,
        userId)
