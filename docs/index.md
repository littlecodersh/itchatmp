# itchatmp

![py27][py27] ![py35][py35] [English version][english-version]

itchatmp是一个开源的微信公众号、企业号接口，使用python调用微信公众号从未如此简单。

基于tornado框架，轻松满足效率需求。支持普通使用、nginx反向代理与wsgi。

同样的命令，支持同步与协程调用，适合各层次开发者使用。

与个人号接口[itchat][itchat]共享类似的操作方式，学习一次掌握两个工具。

## 安装

可以通过本命令安装itchatmp：

```python
pip install itchatmp
```

## 快速入门

有了itchatmp，如果你想要回复发给自己的文本消息，只需要这样：

```python
import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='yourToken',
    appId = 'yourAppId',
    appSecret = 'yourAppSecret'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    return msg['Content']

itchatmp.run()
```

一些进阶应用可以在Advanced uses中看到，或者你也可以阅览[文档][document]。

## 演示机器人

这是一个基于这一项目的开源小机器人，百闻不如一见，有兴趣可以尝试一下。

![QRCode][robot-qr]

## 截屏

![demo][demo]

## 进阶使用

### 企业号配置

在配置时设置copId而非appId即可。

另，由于企业号没有明文模式，所以必须将加密模式设置为安全。

具体的设置可以看[这里][document-enterprise]。

### 协程使用

如果你需要使用协程版本的itchatmp，你需要另外安装一个组件：

```python
pip install itchatmphttp
```

这样，你的itchatmp就变成协程版本了。同样，删除以后就变回了线程池版本。

例如回复信息的操作，协程也只需要这样写：

```python
import itchatmp
from tornado import gen

itchatmp.update_config(itchatmp.WechatConfig(
    token='yourToken',
    appId = 'yourAppId',
    appSecret = 'yourAppSecret'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    yield gen.sleep(3)
    r = yield itchatmp.send('First message', msg['FromUserName'])
    print('First message sent: %s' % r)
    yield gen.sleep(3)
    r = yield itchatmp.send('First message', msg['FromUserName'])
    print('Second message sent: %s' % r)

itchatmp.run()
```

itchatmp里面所有的方法都变成了协程方法，如果你不熟悉协程**建议不要使用**，线程池也足够满足普通需求。

如果你问出类似为什么`time.sleep`阻塞了协程的问题，我会很困扰的。

### WSGI使用

如果你需要生成一个能够在类似SAE的平台上包装的应用，你可以这样生成：

```python
app = itchatmp.run(isWsgi=True)
```

如果你还是无法配置，请阅读文档一栏的[部署][document-deploy]部分。

## 意见与建议

如果有什么问题或者建议都可以在这个[Issue][issue#1]和我讨论

当然也可以加入我们新建的QQ群讨论：438747166

[py27]: https://img.shields.io/badge/python-2.7-ff69b4.svg
[py35]: https://img.shields.io/badge/python-3.5-red.svg
[english-version]: https://github.com/littlecodersh/itchatmp/blob/master/README_EN.md
[itchat]: https://github.com/littlecodersh/itchat
[document]: http://itchatmp.readthedocs.io/zh_CN/latest/
[document-enterprise]: http://itchatmp.readthedocs.io/zh_CN/latest/intro/enterprise/
[robot-qr]: http://7xrip4.com1.z0.glb.clouddn.com/MyPlatform%2F%E6%BC%94%E7%A4%BA%E4%BA%8C%E7%BB%B4%E7%A0%81.jpg?imageView/2/w/200/
[demo]: http://7xrip4.com1.z0.glb.clouddn.com/MyPlatform%2F%E5%85%AC%E4%BC%97%E5%8F%B7%E6%BC%94%E7%A4%BA.png?imageView/2/w/200/
[document-deploy]: http://itchatmp.readthedocs.io/zh_CN/latest/other/deploy/
[issue#1]: https://github.com/littlecodersh/itchatmp/issues/1
