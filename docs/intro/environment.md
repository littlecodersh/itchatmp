这篇内容主要介绍了如何搭建测试的微信号以及正确的联网环境。

如果你已经有了公众号开发经验，那这一部分完全可以跳过不看。

## 获取测试微信号

通过在[这个网址][test-mp]登陆，扫码以后你就获取了一个测试微信公众号。

这样不仅省去了注册和认证的麻烦，接口的调用限制也更少一些。

如果你完成了注册，你会看到这样的页面：（[点这里查看][test-mp-website]）

记住这个页面（之后我会称他为微信测试号页面），之后我们说到的所有的账号相关的内容这里都有。

## 搭建本地测试环境

我们都知道使用微信公众号需要一个独立的网址用于接收信息，但很多时候我们并没有这样的条件。

如果你使用linux，那我就不乱指导你我喜欢怎么配置了。

如果你使用Windows，我这里推荐你使用[natapp这个软件][natapp]。

下载好之后双击`natapp.exe`你就获取了一个独立的网址，非常方便。

如图，红框的内容就是你获得的独立网址。

![][natapp-demo]

## 配置网址

之后我们就需要告诉微信的后台我们的独立网址了。

你可以在微信测试号页面找到“接口配置信息”一栏，这几个字边上有个修改。

点击修改，URL栏里填写你获得的独立网址（可能你每次开natapp都会变，所以如果变了再改咯）。

Token栏里面填写一个用来验证相互身份的内容，我们就写testitchatmp好了（其实可以乱写）。

先不要点击提交，因为提交后服务器会验证你的独立网址是否返回了正确内容，而我们还没有打开我们的项目。

所以这一章结束了，我们获取了我们所需要的环境和各种量，之后我会来指导你完成项目的配置。

[test-mp]: http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login
[test-mp-website]: http://7xrip4.com1.z0.glb.clouddn.com/itchatmp/docs/test-mp-website.png
[natapp]: https://natapp.cn/
[natapp-demo]: http://7xrip4.com1.z0.glb.clouddn.com/itchatmp/docs/natapp-demo.png
