import pickle, logging

from itchatmp.server import WechatServer

logger = logging.getLogger('itchatmp')

__server = WechatServer.instance()

class AccessTokenStorage(object):
    def get_access_token(self):
        raise NotImplementedError()
    def store_access_token(self, accessToken, expireTime):
        raise NotImplementedError()
    def get_server_list(self):
        raise NotImplementedError()
    def store_server_list(self, serverList, fetchTime):
        raise NotImplementedError()

class TestStorage(AccessTokenStorage):
    ''' storage for test use
        {
            'accessToken': ('', 0),
            'serverList': ([], 0),
        }
    '''
    __storageDict = None
    def __init__(self):
        try:
            with open('storage.pkl', 'rb') as f:
                self.__storageDict = pickle.load(f)
        except:
            logger.debug('storage not found')
            self.__storageDict = {}
    def __store_locally(self):
        try:
            with open('storage.pkl', 'wb') as f:
                pickle.dump(self.__storageDict, f)
        except:
            pass
    def get_access_token(self):
        return self.__storageDict.get('accessToken', ('', 0))
    def store_access_token(self, accessToken, expireTime):
        self.__storageDict['accessToken'] = (accessToken, expireTime)
        self.__store_locally()
        logger.debug('Access token updated')
    def get_server_list(self):
        return self.__storageDict.get('serverList', ([], 0))
    def store_server_list(self, serverList, fetchTime):
        self.__storageDict['serverList'] = (serverList, fetchTime)
        self.__store_locally()
        logger.debug('Server list updated')

if not __server.atStorage: __server.atStorage = TestStorage()
