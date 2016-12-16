# itchatmp

![py27][py27] ![py35][py35] [English version][english-version]

itchatmp is an open-source api for wechat massive platform.

Developing wechat massive platform with python has never been easier.

Based on tornado, efficiency is within a simple fetch.

You may use same command in sync way or coroutine way.

You may use it directly, with nginx or wsgi.

And it's similiar to itchat (api for personal wechat), learn once and get two tools.

So enjoy!

## Installation

itchatmp will be installed using this command:

```python
pip install itchatmp
```

## Simple uses

If you want to reply a message to yourself:

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

Detailed introduction is in Advanced uses and [document][document]

## Have a try

This is a robot based on this project, you may have a try:

![QRCode][robot-qr]

## Screenshots

![demo][demo]

## Advanced uses

### Coroutine uses

If you want to use itchatmp in coroutine way, you need to install another package:

```python
pip install itchatmphttp
```

Also, if you delete this, itchatmp will fall back to sync.

Take reply as example, coroutine version of the is:

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

All the methods in itchatmp will become coroutine.

If you are not familiar with coroutine, I strongly advise you learn it before you try the coroutine version.

I sincerely hope questions like why `time.sleep` stuck the main thread will not happen.

And for sync version, I also add thread pool for you, so don't worry about block too much.

### WSGI使用

If you want to deploy onto platform like SAE, app can be produced like this:

```python
app = itchatmp.run(isWsgi=True)
```

For detailed information, you may need [this part][document-deploy] of the document.

## Comments

If you have any problem or suggestion, contact me on [this issue][issue#1].

Or join our QQ group: 438747166.

[py27]: https://img.shields.io/badge/python-2.7-ff69b4.svg
[py35]: https://img.shields.io/badge/python-3.5-red.svg
[english-version]: https://github.com/littlecodersh/itchatmp/blob/master/README_EN.md
[document]: http://itchatmp.readthedocs.io/zh_CN/latest/
[robot-qr]: http://7xrip4.com1.z0.glb.clouddn.com/MyPlatform%2F%E6%BC%94%E7%A4%BA%E4%BA%8C%E7%BB%B4%E7%A0%81.jpg?imageView/2/w/200/
[demo]: http://7xrip4.com1.z0.glb.clouddn.com/MyPlatform%2F%E5%85%AC%E4%BC%97%E5%8F%B7%E6%BC%94%E7%A4%BA.png?imageView/2/w/200/
[document-deploy]: http://itchatmp.readthedocs.io/zh_CN/latest/other/deploy/
[issue#1]: https://github.com/littlecodersh/itchatmp/issues/1
