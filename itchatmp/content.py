SERVER_URL = 'https://api.weixin.qq.com'

NORMAL, COMPATIBLE, SAFE = 0, 1, 2

TEXT = 'text'
IMAGE = 'image'
VOICE = 'voice'
VIDEO = 'video'
SHORT_VIDEO = 'shortvideo'
LOCATION = 'location'
LINK = 'link'
MUSIC = 'music'
NEWS = 'news'
CARD = 'card'
THUMB = 'thumb'
TRANSFER = 'transfer_customer_service'
class _EVENT(object):
    SUBSCRIBE = 'subscribe'
    SCAN = 'SCAN'
    LOCATION = 'LOCATION'
    CLICK = 'CLICK'
    VIEW = 'VIEW'
    def __eq__(self, other):
        return 'event' == other
EVENT = _EVENT()
ENCRYPT = 'encrypt'

INCOME_MSG = (TEXT, IMAGE, VOICE, VIDEO, SHORT_VIDEO, LOCATION,
    LINK, EVENT, EVENT.SUBSCRIBE, EVENT.SCAN, EVENT.LOCATION,
    EVENT.CLICK, EVENT.VIEW)

OUTCOME_MSG = (TEXT, IMAGE, VOICE, VIDEO, MUSIC, NEWS, CARD)

SERVER_WAIT_TIME = 4.5
