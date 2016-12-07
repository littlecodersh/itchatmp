import hashlib

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
