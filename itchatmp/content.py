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
FILE = 'file'
TRANSFER = 'transfer_customer_service'
class _EVENT(object):
    SUBSCRIBE = 'subscribe'
    SCAN = 'SCAN'
    LOCATION = 'LOCATION'
    CLICK = 'CLICK'
    VIEW = 'VIEW'
    def __eq__(self, other):
        return 'event' == other
    def __hash__(self):
        return hash('event')
EVENT = _EVENT()
ENCRYPT = 'encrypt'

INCOME_MSG = [TEXT, IMAGE, VOICE, VIDEO, SHORT_VIDEO, LOCATION,
    LINK, EVENT]

OUTCOME_MSG = [TEXT, IMAGE, VOICE, VIDEO, MUSIC, NEWS, CARD]
