# 消息管理

本文主要介绍三个接口，与[官方文档][mp-wiki]的位置对应如下：

* send: 消息管理-（综合方法没有对应章节）
* messages.send_all: 消息管理-群发接口
* templatemsgs.send: 消息管理-模板消息接口

## 通用回复接口

微信公众平台有各类回复接口，我这里把他们做了一个包装，看起来就简单很多了。

之前的教程当中我们已经使用过这个接口了：

```python
itchatmp.send('Hello', toUserName)
```

发送文本自然不用多说了，这里就说两件事情：

1. 我将一些奇怪的方法也包含了进去，即使该用户没有回复你每天也能发送一定量的信息
2. 各类消息都能通过这个接口回复，我做一个演示

比如我们现在要发送的图片本地地址为`test.jpg`，mediaId为`picturemediaid123`，那么我们就可以这样发送：

```python
itchatmp.send('@img@test.jpg', toUserName)

# or

itchatmp.send('@img@picturemediaid123', toUserName)

# or

itchatmp.send('@img@', toUserName, mediaId='picturemediaid123')

# or

itchatmp.send({
    'MsgType': itchatmp.content.IMAGE,
    'FileDir': 'test.jpg', }, toUserName)

# or

itchatmp.send({
    'MsgType': itchatmp.content.IMAGE,
    'MediaId': picturemediaid123, }, toUserName)
```

标识符和具体的类型对应见下面：

* IMAGE: img
* VOICE: voc
* VIDEO: vid
* TEXT : txt
* CARD : cad
* MUSIC: msc

## 被动回复

将通用回复接口的第一个值作为返回值返回，就可以实现被动回复。

而回复方法的注册通过装饰符注册。

```python
@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    return msg['Content']
```

所有类型的消息都可以通过这个方法注册，你可以通过如下方法注册所有的消息：

```python
@itchatmp.msg_register(itchatmp.content.INCOME_MSG)
def reply(msg):
    print(msg)
```

## 群发接口

群发接口非常简单，这里只做一个基本的演示。

详细的使用指南可以自行阅读[官方文档][mp-wiki]的内容。

```python
itchatmp.messages.send_all(TEXT, 'this is a sendall')
```

## 模板消息

在微信测试号页面，有一个模板消息接口的栏目，你可以在这里新增一个模板用于测试。

我们新增一个这样的模板，标题可以随便取，内容设置为：

```
{{title.DATA}}
用户姓名：{{user.DATA}}
发送内容：{{content.DATA}}
```

点击提交之后，你可以看到一个模板ID。

之后这样操作即可：

```python
templateId = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
msgDict = {
    'title': 'Title',
    'user': 'User',
    'content': 'Content', }
toUserName = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'

r = itchatmp.templatemsgs.send(templateId, msgDict, toUserName)
print(r)
```

[mp-wiki]: https://mp.weixin.qq.com/wiki
