from itchatmp.content import (TEXT,
    IMAGE, VOICE, VIDEO, MUSIC,
    NEWS, TRANSFER, ENCRYPT)

templateDict = {
    TEXT:
    u'''
    <xml>
    <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
    <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
    <CreateTime>{CreateTime}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{Content}]]></Content>
    </xml>
    ''',
    IMAGE:
    u'''
    <xml>
    <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
    <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
    <CreateTime>{CreateTime}</CreateTime>
    <MsgType><![CDATA[image]]></MsgType>
    <Image>
    <MediaId><![CDATA[{MediaId}]]></MediaId>
    </Image>
    </xml>
    ''',
    VOICE:
    u'''
    <xml>
    <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
    <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
    <CreateTime>{CreateTime}</CreateTime>
    <MsgType><![CDATA[voice]]></MsgType>
    <Voice>
    <MediaId><![CDATA[{MediaId}]]></MediaId>
    </Voice>
    </xml>
    ''',
    VIDEO:
    u'''
    <xml>
    <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
    <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
    <CreateTime>{CreateTime}</CreateTime>
    <MsgType><![CDATA[video]]></MsgType>
    <Video>
    <MediaId><![CDATA[{MediaId}]]></MediaId>
    <Title><![CDATA[{Title}]]></Title>
    <Description><![CDATA[{Description}]]></Description>
    </Video>
    </xml>
    ''',
    MUSIC:
    u'''
    <xml>
    <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
    <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
    <CreateTime>{CreateTime}</CreateTime>
    <MsgType><![CDATA[music]]></MsgType>
    <Music>
    <Title><![CDATA[{Title}]]></Title>
    <Description><![CDATA[{Description}]]></Description>
    <MusicUrl><![CDATA[{MusicUrl}]]></MusicUrl>
    <HQMusicUrl><![CDATA[{HQMusicUrl}]]></HQMusicUrl>
    <ThumbMediaId><![CDATA[{ThumbMediaId}]]></ThumbMediaId>
    </Music>
    </xml>
    ''',
    NEWS:
    u'''
    <xml>
    <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
    <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
    <CreateTime>{CreateTime}</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>{ArticleCount}</ArticleCount>
    <Articles>{Articles}</Articles>
    </xml>
    ''',
    'article':
    u'''
    <item>
    <Title><![CDATA[{Title}]]></Title>
    <Description><![CDATA[{Description}]]></Description>
    <PicUrl><![CDATA[{PicUrl}]]></PicUrl>
    <Url><![CDATA[{Url}]]></Url>
    </item>
    ''',
    TRANSFER:
    u'''
    <xml>
    <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
    <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
    <CreateTime>{CreateTime}</CreateTime>
    <MsgType><![CDATA[transfer_customer_service]]></MsgType>
    </xml>
    ''',
    ENCRYPT: 
    u'''
    <xml>
    <Encrypt><![CDATA[{Encrypt}]]></Encrypt>
    <MsgSignature><![CDATA[{MsgSignature}]]></MsgSignature>
    <TimeStamp>{TimeStamp}</TimeStamp>
    <Nonce><![CDATA[{Nonce}]]></Nonce>
    </xml>
    ''',
}
for k, v in templateDict.items():
    if isinstance(templateDict[k], type(u'')):
        templateDict[k] = v.replace(' ', '').replace('\n', '')
    else:
        for i, item in enumerate(templateDict[k]):
            templateDict[k][i] = item.replace(' ', '').replace('\n', '')

def get_template(msgType):
    return templateDict.get(msgType, '')
