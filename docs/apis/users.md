# 用户管理

本文主要介绍十三个接口，与[官方文档][mp-wiki]的位置对应如下：

* users.get_tags: 用户管理-用户标签管理
* users.delete_tag: 用户管理-用户标签管理
* users.create_tag: 用户管理-用户标签管理
* users.update_tag: 用户管理-用户标签管理
* users.add_users_into_tag: 用户管理-用户标签管理
* users.get_tags: 用户管理-用户标签管理
* users.get_users_of_tag: 用户管理-用户标签管理
* users.delete_users_of_tag: 用户管理-用户标签管理
* users.set_alias: 用户管理-设置用户备注名
* users.get_user_info: 用户管理-获取用户基本信息
* users.get_users: 用户管理-获取用户列表
* users.add_users_into_blacklist: 用户管理-黑名单管理
* users.delete_users_of_blacklist: 用户管理-黑名单管理

## 用户标签管理

用户标签管理的相关操作非常简单，这里写一个简单的示例：

```python
#coding-utf8
import itchatmp

toUserName = 'yourusernamehere'

# 清空所有标签
r = itchatmp.users.get_tags()
for tag in r['tags']:
    id_ = tag['id']
    if id_ != 2:
        r = itchatmp.users.delete_tag(id_)

# 创建标签
r = itchatmp.users.create_tag(u'测试标签')

# 标签更名
r = itchatmp.users.get_tags()
id_ = filter(lambda x: x != 2, [tag['id'] for tag in r['tags']])[0]
r = itchatmp.users.update_tag(id_, u'改名的测试标签')

# 将用户打上标签
r = itchatmp.users.add_users_into_tag(id_, [toUserName])

# 获取用户的标签
r = itchatmp.users.get_tags(toUserName)

# 获取标签的用户
r = itchatmp.users.get_users_of_tag(id_)

# 删除标签内的用户
r = itchatmp.users.delete_users_of_tag(id_, [toUserName])
```

## 设置备注名

每个用户都可以有一个备注名，通过这一方法设置：

```python
r = itchatmp.users.set_alias(userName, 'alias')
```

## 获取用户基本信息

通过id可以获取一个用户的全部信息：

```python
r = itchatmp.user.get_user_info(userName)
```

## 获取用户列表

通过这个方法可以获取你的所有用户：

```python
import itchatmp

nextId = ''
totalUserSet = set()
while 1:
    r = itchatmp.users.get_users(nextId)
    totalUserSet.update(r['data']['openid'])
    if len(totalUserSet) == r['total']:
        break
    else:
        nextId = r['next_openid']
print(totalUserSet)
```

## 黑名单管理

与标签类似，黑名单也是这样处理的：

```python
r = itchatmp.users.add_users_into_blacklist(toUserName)
print(r)
r = itchatmp.users.delete_users_of_blacklist(toUserName)
print(r)
```
[mp-wiki]: https://mp.weixin.qq.com/wiki
