# 自定义菜单

本文主要介绍四个接口，与[官方文档][mp-wiki]的位置对应如下：

* menu.create: 自定义菜单-自定义菜单创建接口
* menu.get: 自定义菜单-自定义菜单查询接口
* menu.delete: 自定义菜单-自定义菜单删除接口
* menu.addconditional: 自定义菜单-个性化菜单接口
* menu.delconditional: 自定义菜单-个性化菜单接口

自定义菜单是微信公众号的一个非常重要的功能，至于自定义菜单是什么，就是下图那个东西。

![menu-demo][menu-demo]

## 基本常识

关于自定义菜单，如果你想要，你可以阅读一下[完整的注意事项][menu-homepage]。

这里把最重要的几个点做一个总结。

未认证的个人号是没有自定义菜单的功能的。

我们自定义菜单有10种事件： 

```
click, view, scancode_push, scancode_waitmsg, pic_sysphoto, pic_photo_or_album, pic_weixin, location_select, media_id, view_limited
```

不用担心，之后我会给你一一做一个演示。

关于版本，除了click, view, media_id, view_limited，其他的菜单仅支持微信iPhone5.4.1以上版本，和Android5.4以上版本的微信用户。

另外，自定义菜单每隔五分钟会在进入公众号界面的时候刷新，如果你想要即时看到效果，重新关注就好了。

## 前期准备

由于这一章我们需要通过菜单给用户发送一些内容，所以我们需要先把这些内容准备一下。

当然这里用到的都是还没有介绍过的功能，这些都会在之后的文档中有一个解释。

首先是上传用的图片素材的MediaId，在本地放置一张`demo.jpg`，之后运行这个程序：

```python
r = itchatmp.messages.upload(IMAGE, 'demo.jpg', permanent=True)
if r:
    r = 'Upload succeeded, media id: ' + r['media_id']
print(r)
```

这串字符就是你需要的MediaId。

菜单需要的是永久素材，当然，不用担心永久素材超过上限，通过这个方法可以删除所有的永久素材。

当然，你现在不需要使用这个方法，只是在这里提一下而已。

```python
r = itchatmp.messages.batchget_material(IMAGE)
if not r: print(r)
for m in r['item']:
    r = itchatmp.messages.delete_material(m['media_id'])
    if not r: print(r)
```

## 创建菜单

如果把菜单变成json的形式，就是下面的样子：

不急着看，复制到程序中即可，之后可以按一个按钮，对照着按钮和返回值看这里的设置。

这里的mediaId就是之前我们获取的图片的永久素材id，复制过来就可以了。

```python
mediaId = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
menu = {'button':[
    {
        'name': '1-5',
        'sub_button': [
            {
                'type': 'click',
                'name': 'click-name',
                'key': 'click-key',
            },
            {
                'type': 'view',
                'name': 'view-name',
                'url':  'http://itchat.cc',
            },
            {
                'type': 'scancode_push',
                'name': 'scancode_push-name',
                'key': 'scancode_push-key',
            },
            {
                'type': 'scancode_waitmsg',
                'name': 'scancode_waitmsg-name',
                'key': 'scancode_waitmsg-key',
            },
            {
                'type': 'pic_sysphoto',
                'name': 'pic_sysphoto-name',
                'key': 'pic_sysphoto-key',
            },
        ],
    },
    {
        'name': '6-10',
        'sub_button': [
            {
                'type': 'pic_photo_or_album',
                'name': 'pic_photo_or_album-name',
                'key': 'pic_photo_or_album-key',
            },
            {
                'type': 'pic_weixin',
                'name': 'pic_weixin-name',
                'key': 'pic_weixin-key',
            },
            {
                'type': 'location_select',
                'name': 'location_select-name',
                'key': 'location_select-key',
            },
            {
                'type': 'media_id',
                'name': 'media_id-name',
                'media_id': mediaId,
            },
        ],
    },
]}
```

然后我们将这段代码放在上面定义menu的下面，运行即可创建菜单。

```python
r = itchatmp.menu.create(menu)
print(r)
```

等一段时间或者重新关注就可以看到自定义菜单刷新了。

最后让我们开启我们的服务器，然后测试每个按钮的返回值吧！

这后面是服务器的代码：

```
@itchatmp.msg_register(itchatmp.content.INCOME_MSG)
def text_reply(msg):
    print('='*20)
    print(msg)

itchatmp.run()
```

运行之后记得对照着每个按键点击之后在命令行上输出的文本看一下那个按键是怎么定义的。

## 获取、删除菜单

这个操作就没有什么可以讲的东西了，直接看代码吧：

```python
r = itchatmp.menu.get()
print(r)
```

而删除就是：

```python
r = itchatmp.menu.delete()
print(r)
```

## 设置个性化菜单

微信还支持对于符合特定条件的人设置不同的菜单。

比如我想要对广州地区的用户设置一个特殊的菜单，那json就应该这样设置：

```python
menu = {
    'button':[
 	{	
    	'type':'click',
    	'name':'你好，广州',
     	'key':'guangzhou' 
	}]
    'matchrule':{ 'city':'广州' }
}
```

然后调用接口即可：

```python
r = itchatmp.menu.addconditional(menu)
print(r)
```

通过普通菜单的获取接口找到自定义菜单的menuId之后，调用接口：

```python
menuId = 0
r = itchatmp.menu.delconditional(menuId)
print(r)
```

到这里你已经能自己创建想要的自定义菜单了（配合返回值的指导）。

[mp-wiki]: https://mp.weixin.qq.com/wiki
[menu-demo]: http://7xrip4.com1.z0.glb.clouddn.com/itchatmp/docs/menu-demo.png?imageView/2/h/200/
[menu-homepage]: https://mp.weixin.qq.com/wiki
