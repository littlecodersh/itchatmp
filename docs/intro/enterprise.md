# 企业号基础配置

企业号由于微信对其的安全考虑，是没有不加密的选项的。

所以即使是测试我们也需要将加密的内容填写上去，即这样更新配置：

```python
itchatmp.update_config(itchatmp.WechatConfig(
    token='testitchatmp',
    copId = 'xxxxxxxxxxxxxxxxxx',
    appSecret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    encryptMode=itchatmp.content.SAFE,
    encodingAesKey='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',))
```

其中encodingAesKey不能乱填，建议使用官网自带的功能生成。

另外，这里**我们输入的是copId**来告诉itchatmp你要用的是企业号。

鉴于开发企业号大都已经有了不错的底子，我这里就不重复出一份引导小白的指南给各位了。

这是itchatmp能够给企业号提供的API：[API 列表][api-list]（在建）

有些不在这个列表里的接口的意思就是，那个接口只有公众号可以使用。

[api-list]: http://itchatmp.readthedocs.io/zh_CN/latest/apilist/qy/
