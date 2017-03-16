import os, logging, traceback
import hashlib, struct
from base64 import b64decode, b64encode

try:
    from Crypto.Cipher import AES
except ImportError:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    def aes_encode(key, data):
        cryptor = Cipher(algorithms.AES(key), modes.CBC(key[:16]),
            backend=default_backend()).encryptor()
        return b64encode(cryptor.update(data) + cryptor.finalize())
    def aes_decode(key, data):
        cryptor = Cipher(algorithms.AES(key), modes.CBC(key[:16]),
            backend=default_backend()).decryptor()
        return cryptor.update(b64decode(data)) + cryptor.finalize()
else:
    def aes_encode(key, data):
        cryptor = AES.new(key, AES.MODE_CBC, key[:16])
        return b64encode(cryptor.encrypt(data))
    def aes_decode(key, data):
        cryptor = AES.new(key, AES.MODE_CBC, key[:16])
        return cryptor.decrypt(b64decode(data))

from itchatmp.content import ENCRYPT
from itchatmp.views import deconstruct_msg, construct_msg

logger = logging.getLogger('itchatmp')

def decrypt_msg(timestamp, nonce, signature, config, msgDict):
    ''' decrypt msg from wechat, use AES_CBC decryption
        return a dict contains encrypted information
        if decrypt failed, will return an empty dict
        pass {'echostr': ECHOSTR} into msgDict to decrypt Cop mp oauth
    '''
    if 'echostr' in msgDict:
        msgDict['Encrypt'] = msgDict['echostr']
    elif msgDict.get('MsgType') != ENCRYPT:
        return msgDict
    try:
        text = aes_decode(config._encodingAesKey, msgDict['Encrypt'])
        text = text[16:-(text[-1] if isinstance(text[-1], int) else ord(text[-1]))]
        xmlLen = struct.unpack('>I', text[:4])[0]
        xmlContent = text[4:xmlLen + 4].decode('utf8')
        fromAppid = text[xmlLen + 4:].decode('utf8')
    except:
        logger.debug(traceback.format_exc())
        return {}
    # Check appId
    if fromAppid not in (config.appId, config.copId):
        logger.debug('A message from wrong appid is filtered when decrypt: %s' % fromAppid)
        return {}
    if 'echostr' in msgDict:
        return {'echostr': xmlContent}
    else:
        return deconstruct_msg(xmlContent)

def encrypt_msg(timestamp, nonce, signature, config, replyDict):
    ''' encrypt msg for sending to wechat
     * use AES_CBC encryption
     * return a string ready for sending
     * as in construct_msg, string in replyDict should be unicode
    '''
    text = construct_msg(replyDict).encode('utf8')
    text = os.urandom(16) + struct.pack('>I', len(text)) +\
        text + config.appId.encode('utf8')
    paddingAmount = 32 - (len(text) % 32)
    text += chr(paddingAmount).encode('utf8') * paddingAmount
    text = aes_encode(config._encodingAesKey, text)
    # Encrypt generated
    s = [i.encode('utf8') for i in (timestamp, nonce, config.token)]
    s += [text]; s.sort(); s = b''.join(s)
    # Signature generated
    return construct_msg({
            'FromUserName': replyDict['FromUserName'],
            'ToUserName': replyDict['ToUserName'],
            'MsgType': ENCRYPT,
            'Encrypt': text.decode('utf8'),
            'MsgSignature': hashlib.sha1(s).hexdigest(),
            'TimeStamp': timestamp,
            'Nonce': nonce,
        }, )

def oauth(timestamp, nonce, signature, token, echostr=None):
    ''' determine whether signature of request is right
     * both get and post functions need oauth
     * msgs we generate for sending don't match this fn
     * for Cop mp, we need echostr as well
    '''
    s = [timestamp, nonce, token]
    if echostr is not None: s.append(echostr)
    s.sort(); s = ''.join(s).encode('utf8')
    return hashlib.sha1(s).hexdigest() == signature
