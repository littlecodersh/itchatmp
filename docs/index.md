# itchatmp

![py27][py27] ![py35][py35]

itchatmp是一个开源的微信公众号接口，使用python调用微信公众号从未如此简单。

itchatmp基于tornado框架，满足效率需求。支持普通使用、nginx反向代理与wsgi。

## Installation

可以通过本命令安装itchatmp：

```python
pip install itchatmp
```

## Simple uses

有了itchatmp，如果你想要回复发给自己的文本消息，只需要这样：

```python
import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='yourToken',
    appId = 'yourAppId',
    appSecret = 'yourAppSecret'))

@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    return msg['content']

itchatmp.run()
```

一些进阶应用可以在Advanced uses中看到，或者你也可以阅览[文档][document]。

## Have a try

这是一个基于这一项目的开源小机器人，百闻不如一见，有兴趣可以尝试一下。

![QRCode][robot-qr]

## Screenshots

![demo][demo]

## Advanced uses

Building

## Comments

如果有什么问题或者建议都可以在这个[Issue][issue#1]和我讨论

当然也可以加入我们新建的QQ群讨论：438747166

[py27]: https://img.shields.io/badge/python-2.7-ff69b4.svg
[py35]: https://img.shields.io/badge/python-3.5-red.svg
[english-version]: https://github.com/littlecodersh/itchatmp/blob/master/README_EN.md
[document]: https://itchat.readthedocs.org/zh/latest/
[robot-qr]: http://7xrip4.com1.z0.glb.clouddn.com/MyPlatform%2F%E6%BC%94%E7%A4%BA%E4%BA%8C%E7%BB%B4%E7%A0%81.jpg?imageView/2/w/200/
[demo]: http://7xrip4.com1.z0.glb.clouddn.com/MyPlatform%2F%E5%85%AC%E4%BC%97%E5%8F%B7%E6%BC%94%E7%A4%BA.png?imageView/2/w/200/
[issue#1]: https://github.com/littlecodersh/itchatmp/issues/1
