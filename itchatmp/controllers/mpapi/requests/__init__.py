import json

from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine, Return

import requests

if __name__ == '__main__':
    class requests(object):
        @coroutine
        def get(self, url):
            r = AsyncHTTPClient().fetch(url)
            raise Return(Response(r.body))
        @coroutine
        def post(self, url, data):
            httpClient = AsyncHTTPClient()
            data = json.dumps(data)
            if not isinstance(data, bytes):
                data = data.encode('utf8', 'replace')
            headers = {'Content-Type': 'application/json'}
            r = httpClient.fetch(url, method='POST', body=data, headers=headers)
            raise Return(Response(r.body))
    class Response(object):
        def __init__(self, content):
            self.content = content
        def json(self):
            try:
                return json.loads(self.content.decode('utf8'))
            except:
                print('decode error')
            return json.loads(self.content)
