class ItChatException(Exception):
    ''' exception base '''
    pass

class ItChatSDKException(ItChatException):
    ''' SDK error '''
    def __init__(self, message=''):
        self.message = message
    def __str__(self):
        return self.message

class ItChatEnvException(ItChatException):
    ''' SDK error '''
    def __init__(self, message=''):
        self.message = message
    def __str__(self):
        return self.message
