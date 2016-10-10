class BaseException(Exception):
    ''' exception base '''
    pass

class ParameterError(BaseException):
    def __init__(self, message=''):
        self.message = message
    def __str__(self):
        return self.message

class EnvironmentError(BaseException):
    def __init__(self, message=''):
        self.message = message
    def __str__(self):
        return self.message
