import hashlib

def oauth(timestamp, nonce, signature, token):
    s = [timestamp, nonce, token]
    s.sort(); s = ''.join(s)
    return hashlib.sha1(s).hexdigest() == signature
