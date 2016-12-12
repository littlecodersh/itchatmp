import json

from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine, Return

# if you have itchatmphttp installed
# we will use coroutine requests instead
try:
    from itchatmphttp import requests
except ImportError:
    import requests
