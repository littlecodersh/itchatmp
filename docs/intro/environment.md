# 基础环境配置

这篇内容主要介绍了如何搭建测试的微信号以及正确的联网环境。

如果你已经有了公众号开发经验，那这一部分完全可以跳过不看。

如果你使用的是企业公众号，想必你也已经有了一定的开发经验，我可能需要多嘴说两句的内容我都写在[这里][enterprise.md]了。

## 获取测试微信号

通过在[这个网址][test-mp]登陆，扫码以后你就获取了一个测试微信公众号。

这样不仅省去了注册和认证的麻烦，接口的调用限制也更少一些。

如果你完成了注册，你会看到这样的页面：（[点这里查看][test-mp-website]）

记住这个页面（之后我会称他为**微信测试号页面**），之后我们说到的所有的账号相关的内容这里都有。

## 搭建本地测试环境

我们都知道使用微信公众号需要一个独立的网址用于接收信息，但很多时候我们并没有这样的条件。

如果你使用linux，那我就不乱指导你我喜欢怎么配置了。

如果你使用Windows，我这里推荐你使用[natapp这个软件][natapp]。

下载好之后双击`natapp.exe`你就获取了一个**独立网址**，非常方便。

如图，红框的内容就是你获得的独立网址，**请不要关闭natapp直到你不再需要使用这个独立网址为止**。

![][natapp-demo]

## 配置网址

之后我们就需要告诉微信的后台我们的独立网址了。

你可以在微信测试号页面找到“接口配置信息”一栏，这几个字边上有个修改。

点击修改，URL栏里**填写你获得的独立网址**（可能你每次开natapp都会变，所以如果变了再改咯）。

Token栏里面填写一个用来验证相互身份的内容，**我们就写testitchatmp好了**（其实可以乱写）。

先不要点击提交，因为提交后服务器会验证你的独立网址是否返回了正确内容，而我们还没有打开我们的项目。

## 启动你的项目并完成配置

如果你没有安装我们的项目，请先通过如下方法在命令行安装：

```bash
pip install itchatmp -U
```

下面我们需要启动我们的项目，请确保本机的80端口没有被占用且有权限使用。

将如下程序创建为`main.py`，其中**appId和appSecret需要修改**，在微信测试号页面你可以找到，剩下的不用改即可。

```python
import itchatmp

itchatmp.update_config(itchatmp.WechatConfig(
    token='testitchatmp',
    appId = 'xxxxxxxxxxxxxxxxxx',
    appSecret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'))

itchatmp.run()
```

之后在命令行运行该程序：

```bash
python main.py
```

你将会看到itchatmp启动的提示。

我们访问一下我们通过natapp获得的独立网址，你将会看到`Greeting from itchatmp!`。

这是你就可以点击上一步的提交了，你将看到配置成功的消息。

如果没有请检查一下各个内容是否填写完整。

所以这一章结束了，我们获取了我们所需要的环境和各种量，之后我会来指导你就项目做一些简单的入门操作。

[enterprise.md]: http://itchatmp.readthedocs.io/zh_CN/latest/intro/enterprise/
[test-mp]: http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login
[test-mp-website]: http://7xrip4.com1.z0.glb.clouddn.com/itchatmp/docs/test-mp-website.png
[natapp]: https://natapp.cn/
[natapp-demo]: http://7xrip4.com1.z0.glb.clouddn.com/itchatmp/docs/natapp-demo.png
