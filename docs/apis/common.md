# 通用接口

本文主要介绍四个接口，与[官方文档][mp-wiki]的位置对应如下：

* set_logging: 为itchatmp提供的功能
* access_token: 开始开发-获取access_token
* get_server_ip: 开始开发-获取微信服务器IP地址
* clear_quota: 开始前必读-接口调用频次限制说明

access_token是公众号的全局唯一接口调用凭据，公众号调用各接口时都需使用access_token。

这部分以get_server_ip为例子，介绍如何使用access_token，以及itchatmp内部access_token存储原理。

## set_logging使用简介

虽然你可以通过logging实现各式各样的日志设置，但也许提供一个简单的接口可以节省你一点时间。

如果你想要过滤掉低于INFO等级的日志后在本地`itchatmp.log`文件存储日志并输出到控制台：

```python
import logging

itchatmp.set_logging(showOnCmd=True, loggingFile=None, loggingLevel=logging.INFO)
```

建议在定义所有内容之前定义这一句，否则可能漏掉日志。

当然，这三项都是可选的，不需要留空即可。

## clear_quota使用简介

每一个接口的调用都是有每日次数的限制的，但如果不小心因为程序错误把一天的量都跑完了怎么办呢？

你也可以重置这个限制，每个月有五次重置的机会，所以谨慎使用这个方法吧。

另外，在测试的账号中是无法使用这个接口的，所以测试的时候跳过就好了。

```python
itchatmp.clear_quota()
```

## access_token使用简介

access_token在itchatmp中被做成了一个装饰器的形式。

将会给装饰的函数附一个键名为accessToken的值，内容及字符串形式的accessToken。

注意，import和update_config部分由于在入门部分已经讲过，之后的程序都不会重写这部分。

```python
@itchatmp.access_token
def get_access_token(accessToken=None):
    return accessToken

r = get_access_token()
print(r)
```

如果你声明的函数需要itchatmp给予accessToken的配合，那么也是同样的写法。

## get_server_ip使用简介

具体的使用你打印一下结果即可，另，关于之后的输出也可以参考这样：

```
import logging

logger = logging.getLogger('itchatmp')

r = itchatmp.common.get_server_ip()
logger.info(r)
```

可能值得一讲的是如何实现的get_server_ip，权当是对于accessToken使用的演示：

```python
import requests

SERVER_URL = 'https://api.weixin.qq.com'

@itchatmp.access_token
def get_server_ip(accessToken=None)
    url = '%s/cgi-bin/getcallbackip?access_token=%s' % \
        (SERVER_URL, accessToken)
    return requests.get(url).json()
```

简而言之就是这样。

## 过滤非微信服务器信息

既然能够获得服务器的ip地址，那么显而易见可以做的一件事情就是过滤非服务器ip的消息。

我已经帮你做好了这份工作，你只需要这样设置：

```python
itchatmp.update_config(filterRequest=True)
```

当然，如果你在Windows下通过natapp转发，那肯定是无法开启这个功能了。

## accessToken存储方式

如果你不设置的话默认会将accessToken存储在本地，当然你也可以自己继承一个存储的类：

```python
class Storage(itchatmp.models.AccessTokenStorage):
    def get_access_token(self):
        pass
    def store_access_token(self, accessToken, expireTime):
        pass
    def get_server_list(self):
        pass
    def store_server_list(self, serverList, fetchTime):
        pass
```

每次更新accessToken和服务器列表的时候都会调用存储方法。

[mp-wiki]: https://mp.weixin.qq.com/wiki
