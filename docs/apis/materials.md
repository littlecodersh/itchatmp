# 素材管理

本文主要介绍八个接口，与[官方文档][mp-wiki]的位置对应如下：

* messages.upload: 素材管理-新增临时素材、新增永久素材
* messages.create_news: 素材管理-新增图文素材
* messages.download: 素材管理-获取临时素材
* messages.get_material: 素材管理-获取永久素材
* messages.get_material_count: 素材管理-获取素材总数
* messages.batchget_material: 素材管理-获取素材列表
* messages.delete_material: 素材管理-删除永久素材
* messages.update_news: 素材管理-修改永久图文素材

## 新增素材

在微信公众平台中我们可以上传四种类型的素材，其限制如下：

* 图片（image）: 2M，支持PNG\JPEG\JPG\GIF格式
* 语音（voice）：2M，播放长度不超过60s，支持AMR\MP3格式
* 视频（video）：10MB，支持MP4格式
* 缩略图（thumb）：64KB，支持JPG格式

如果你上传素材并希望他是临时的可以使用这个方法：

```python
import itchatmp

r = itchatmp.messages.upload(itchatmp.content.IMAGE, 'myimage.jpg')
if r:
    print(r['media_id'])
else:
    print('Failed: \n%s' % r)
```

临时的素材可以在服务器上保存三天，而我们打印出来的值就是我们之后使用这个素材的凭证了。

其中新闻素材比较特殊，这里也做一个演示：

```python
#coding=utf8
import itchatmp

r = itchatmp.messages.upload(itchatmp.content.THUMB, 't.jpg')
infoDict = {
  "articles": [{
       "title": u'标题',
       "thumb_media_id": r['media_id'],
       "author": u'作者',
       "digest": u'摘要',
       "show_cover_pic": 1,
       "content": u'内容',
       "content_source_url": 'http://www.bing.com'
    },
 ]
}

r = itchatmp.messages.create_news(infoDict)
```

当然你也可以上传永久的素材，除了上述的四种类型也是同样的限制和调用方法：

```python
import itchatmp

r = itchatmp.messages.upload(itchatmp.content.IMAGE, 'myimage.jpg', permanent=True)
if r:
    print(r['media_id'])
else:
    print('Failed: \n%s' % r)
```

永久素材是有数量限制的，图文消息素材、图片素材上限为5000，其他类型为1000。

值得注意的是，永久素材的图片除了media_id之外还会获取一个图片的url。

另外，永久素材的视频需要额外的两个键值：

```python
infoDict = {
    'Title' : u'标题',
    'Description' : u'简介', }
r = itchatmp.messages.upload(itchatmp.content.VIDEO, 'myvideo.mp4',
    additionalDict=infoDict, permanent=True)
```

另外，如果你的永久图文素材里面用到了图片，也必须确保是永久图片，否则会无法生成。

## 下载素材

无论是临时素材还是永久素材都有一个标识符，都可以通过如下方法下载：

临时素材：

```python
import itchatmp

mediaId = 'yourmediaid'
r = itchatmp.messages.download(mediaId)
if 'File' in r:
    with open(r.get('FileName', 'myfile'), 'wb') as f:
        f.write(r['File'].getvalue())
else:
    print(r)
```

其中如果是视频文件，将会返回一个url用于自行控制如何下载。

永久素材：

```python
import itchatmp

mediaId = 'yourmediaid'
r = itchatmp.messages.get_material(mediaId)
if 'File' in r:
    with open(r.get('FileName', 'myfile'), 'wb') as f:
        f.write(r['File'].getvalue())
else:
    print(r.get('url', r))
```

## 控制永久素材

由于永久素材存在数量限制，所以我们需要控制永久素材的数量，及时删除不需要的素材。

通过这个方法可以获取永久素材的数量：

```python
import itchatmp
r = itchatmp.messages.get_material_count()
print(r)
```

具体的每种类型素材的列表则这样获取：

```python
import itchat
r = itchatmp.messages.batchget_material(itchatmp.content.VIDEO, offset=0, count=20)
print(r)
```

然后将不需要的素材删除即可：

```python
import itchat
r = itchatmp.messages.delete_material(mediaId)
print(r)
```

其中永久的图文素材是可以修改的：

```python
#coding=utf8
import itchatmp

mediaId = 'mynewsmediaid'
thumbId = 'mythumbid'

infoDict = {
    "articles": [{
        "title": u'标题',
        "thumb_media_id": thumbId,
        "author": u'作者',
        "digest": u'摘要',
        "show_cover_pic": 1,
        "content": u'内容',
        "content_source_url": 'http://www.bing.com' }, ] }

r = itchatmp.messages.update_news(mediaId, infoDict, index=0)
```
[mp-wiki]: https://mp.weixin.qq.com/wiki
