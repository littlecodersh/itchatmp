VERSION = '0.0.17'

SERVER_URL = 'https://api.weixin.qq.com'
COMPANY_URL = 'https://qyapi.weixin.qq.com'

SERVER_WAIT_TIME = 4.5

GREETING_WORDS = 'Greeting from itchatmp!'

try:
    import itchatmphttp
    COROUTINE = True
except ImportError:
    COROUTINE = False
