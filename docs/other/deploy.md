# 部署

## 部署到SAE

部署到SAE需要配置四样东西：

不过首先，我们先将SAE的代码目录克隆到本地（记得把下面的命令中的地址改了）并**进入该目录**。

```bash
git clone https://git.sinacloud.com/youritchatmptest
cd youritchatmptest
```

### 第三方包安装

由于SAE提供的自带第三方包有限，所以我们需要自己安装一些：

```bash
pip install itchatmp -t vendor
```

### 设置程序入口

我们在该目录下新建一个文件`index.wsgi`，输入如下内容：

```python
import sae

# site-packages
sae.add_vendor_dir('vendor')

from main import app
application = sae.create_wsgi_app(app)
```

### 设置SAE配置文件

我们在该目录下新建一个文件`config.yaml`，输入如下内容：

```yaml
name: youritchatmptest
version: 1
libraries:
- name: lxml
  version: '2.3.4'
- name: PyCrypto
  version: '2.6'
```

### 设置主程序

最后，我们将主程序写好：

```python
import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='xxxxxxxxxxxxxxxxxxxxxx',
    appId = 'xxxxxxxxxxxxxxxxxx',
    appSecret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'),
    itchatmp.models.common.MemCacheStorage())

itchatmp.set_logging(loggingLevel=10)

@itchatmp.msg_register(itchatmp.content.INCOME_MSG)
def text_reply(msg):
    return msg

app = itchatmp.run(isWsgi=True)
```

### 另

最后我们把程序上传上去即可。

记得SAE需要实名制才能完成认证，否则会由于SAE向网页中插入了内容而认证失败。

由于SAE缺少必要的组件，所以itchatmphttp就不要装了，没有办法使用的。
