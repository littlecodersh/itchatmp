import os
import hashlib, socket, struct
from base64 import b64decode, b64encode

from Crypto.Cipher import AES

from itchatmp.content import ENCRYPT
from itchatmp.views import deconstruct_msg, construct_msg

def oauth(timestamp, nonce, signature, token):
    s = [timestamp, nonce, token]; s.sort()
    s = ''.join(s).encode('utf8')
    return hashlib.sha1(s).hexdigest() == signature

def decrypt_msg(timestamp, nonce, signature, config, msgDict):
    if not msgDict.get('MsgType') == ENCRYPT: return
    # Check msgType
    # s = [timestamp, nonce, config.token, msgDict['Encrypt']]
    # s.sort(); s = ''.join(s).encode('utf8')
    # Check signature
    cryptor = AES.new(config._encodingAesKey,
        AES.MODE_CBC, config._encodingAesKey[:16])
    text = cryptor.decrypt(b64decode(msgDict['Encrypt']))
    text = text[16:-ord(text[-1])]
    xmlLen = socket.ntohl(struct.unpack('I', text[:4])[0])
    xmlContent = text[4:xmlLen + 4]
    fromAppid = text[xmlLen + 4:]
    if fromAppid != config.appId: return
    # Check appId
    return deconstruct_msg(xmlContent)

def encrypt_msg(timestamp, nonce, signature, config, msgDict, replyDict):
    text = construct_msg(msgDict, replyDict)
    text = os.urandom(16) + struct.pack('I', socket.htonl(len(text))) +\
        text.encode('utf8') + config.appId.encode('utf8')
    paddingAmount = 32 - (len(text) % 32)
    text += chr(paddingAmount).encode('utf8') * paddingAmount
    cryptor = AES.new(config._encodingAesKey,
        AES.MODE_CBC, config._encodingAesKey[:16])
    text = b64encode(cryptor.encrypt(text))
    # s = [timestamp, nonce, config.token, text]
    # s.sort(); s = ''.join(s).encode('utf8')
    s = [i.encode('utf8') for i in (timestamp, nonce, config.token)]
    s += [text]; s.sort(); s = b''.join(s)
    return construct_msg(msgDict,
        {
            'MsgType': ENCRYPT,
            'Encrypt': text,
            'MsgSignature': hashlib.sha1(s).hexdigest(),
            'TimeStamp': timestamp,
            'Nonce': nonce,
        }, )
