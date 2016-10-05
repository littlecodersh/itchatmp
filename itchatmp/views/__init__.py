import time
import xml.etree.ElementTree as ET

from ..content import TEXT
from .templates import get_template

def deconstruct_msg(msg):
    r = {}
    msg = ET.fromstring(msg)
    for i in msg: r[i.tag] = i.text
    return r

def construct_msg(msgType, msgDict, replyDict):
    return get_template(msgType) % (
        msgDict['FromUserName'], msgDict['ToUserName'],
        int(time.time()), msgType, replyDict['Content'])
