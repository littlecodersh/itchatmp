import logging

class LogSystem(object):
    handlerList = []
    showOnCmd = True
    loggingLevel = logging.INFO
    loggingFile = None
    def __init__(self):
        self.cmdHandler = None
        for handler in logging.getLogger().handlers:
            if 'StreamHandler' in str(handler):
                self.cmdHandler = handler
        if self.cmdHandler is None:
            self.cmdHandler = logging.StreamHandler()
            logging.getLogger().addHandler(self.cmdHandler)
        self.logger = logging.getLogger('itchatmp')
        self.logger.addHandler(logging.NullHandler())
        self.logger.setLevel(self.loggingLevel)
        self.fileHandler = None
    def set_logging(self, showOnCmd=True, loggingFile=None,
            loggingLevel=logging.INFO):
        if showOnCmd != self.showOnCmd:
            if showOnCmd:
                logging.getLogger().addHandler(self.cmdHandler)
            else:
                logging.getLogger().removeHandler(self.cmdHandler)
            self.showOnCmd = showOnCmd
        if loggingFile != self.loggingFile:
            if self.loggingFile is not None: # clear old fileHandler
                self.logger.removeHandler(self.fileHandler)
                self.fileHandler.close()
            if loggingFile is not None: # add new fileHandler
                self.fileHandler = logging.FileHandler(loggingFile)
                self.logger.addHandler(self.fileHandler)
            self.loggingFile = loggingFile
        if loggingLevel != self.loggingLevel:
            self.logger.setLevel(loggingLevel)
            self.loggingLevel = loggingLevel

ls = LogSystem()
set_logging = ls.set_logging
