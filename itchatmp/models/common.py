import pickle, logging, sys

logger = logging.getLogger('itchatmp')

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

class MemCacheStorage(AccessTokenStorage):
    ''' storage for memcache
        'accessToken': ('', 0),
        'serverList': ([], 0),
    '''
    def __init__(self):
        try:
            import pylibmc
        except ImportError:
            logger.info('pylibmc is not installed')
            sys.exit()
        self.__storage = pylibmc.Client()
    def get_access_token(self):
        return self.__storage.get('accessToken') or ('', 0)
    def store_access_token(self, accessToken, expireTime):
        self.__storage.set('accessToken', (accessToken, expireTime))
        logger.debug('Access token updated')
    def get_server_list(self):
        return self.__storage.get('serverList') or ([], 0)
    def store_server_list(self, serverList, fetchTime):
        self.__storage.set('serverList', (serverList, fetchTime))
        logger.debug('Server list updated')
