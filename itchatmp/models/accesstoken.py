import pickle, logging

logger = logging.getLogger('itchatmp')

class TmpStorage(object):
    ''' storage for test use
        {
            'accessToken': ('', 0),
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

__storage = TmpStorage()

def get_access_token():
    return __storage.get_access_token()

def store_access_token(accessToken, expireTime):
    return __storage.store_access_token(accessToken, expireTime)
