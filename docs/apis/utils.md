# 小工具

本文主要介绍三个接口，与[官方文档][mp-wiki]的位置对应如下：

* utils.create_qrcode: 账号管理-生成带参数的二维码
* utils.download_qrcode: 账号管理-生成带参数的二维码
* utils.long_url_to_short: 账号管理-长链接转短链接接口

## 带参数二维码

当用户扫描相应的二维码的时候公众号将会收到二维码事件并在事件中带有这里设定的参数。

`create_qrcode`可以设定两个参数，数据与过期时间。

如果你需要你的二维码永不过期，设定`expire=False`即可。

关于数据，如果你的二维码是会过期的，那数据可以是字符串或者是数字。

否则的话只能是数字。

```python
r = itchatmp.utils.create_qrcode('test-tag', expire=5000)
print(r)
```

通过获取的ticket可以下载相应的二维码：

```python
r = itchatmp.utils.download_qrcode(ticket)
print(r)
```

## 长链接转短链接

就如字面意思，该接口可以将长链接转为短链接。

```python
r = itchatmp.utils.long_url_to_short('http://www.sogou.com')
print(r)
```

[mp-wiki]: https://mp.weixin.qq.com/wiki
