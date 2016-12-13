# 快速入门

欢迎你来了解我为你准备的微信公众号开发的方式。

我很喜欢这个方式，我给他起名为itchatmp，希望你也能喜欢。

通过这个方式开发微信公众号，所有奇怪的细节都被隐藏在简洁的表面下面。

你不用考虑处理的阻塞、http的交互，你要做的就是调用一些简单的API。

那么让我们开始吧！

## 发送一条最简单的欢迎信息

首先你需要先完成环境的搭建，你所需要的内容我都在[这里]为你写好了。

之后我们关注一下我们申请到的测试微信号，二维码在微信测试号页面可以找到，扫码关注即可。

关注后，你可以在二维码边上看到你的用户信息（看不到的话刷新一下即可）。

![][userid-website]

例如我的微信号（不是常规你认识的那个微信号）就是`littlecoderuserid`。

**这个值我们之后称为userId**，是公众号用户的唯一标示符。

最后我们运行发送给这个微信用户一条信息的程序，具体而言：

你需要将如下内容写到你的程序中，比如，我们将程序命名为`main.py`。

appId和appSecret需要修改，怎么填写在环境配置的时候也有提过，之后不再赘述。

userId要改成你看到的你自己的userId，这个之后也不再提醒。

```python
import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='testitchatmp',
    appId = 'xxxxxxxxxxxxxxxxxx',
    appSecret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'))

userId = 'littlecoderuserid'
r = itchatmp.send('greeting from itchatmp!', userId)
print(r)
```

看一下你的手机，你是不是收到了一条来自测试微信号的消息？

这里有两点值得提示，一是你实际上从未给这个微信号发送过消息。

如果你了解微信公众平台，应该可以看出我后台为你做了很多事情。

二是，如果是中文的话记得发送unicode的字符串。

```python
r = itchatmp.send(u'你好', userId)
```

## 做一个简单的交互

一般来说我们熟悉的与公众号之间的交流都是以公众号实时回复的形式完成的。

那么按我们的方式，这件事情是这样完成的：

```python
import itchatmp
from itchatmp.content import TEXT

itchatmp.update_config(itchatmp.WechatConfig(
    token='testitchatmp',
    appId = 'xxxxxxxxxxxxxxxxxx',
    appSecret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    print(msg)
    return 'I received: ' + msg['Text']

itchatmp.run()
```

运行一下说句话吧。

更多关于itchatmp的内容，欢迎你继续阅读进阶篇的内容！

[environment.md]: http://itchatmp.readthedocs.io/zh_CN/latest/intro/environment/
[userid-website]: http://7xrip4.com1.z0.glb.clouddn.com/itchatmp/docs/userid-website.png
