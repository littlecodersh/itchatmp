import logging

logger = logging.getLogger('itchatmp')

logger.setLevel(logging.DEBUG)

cmdHandler = logging.StreamHandler()
cmdHandler.setLevel(logging.DEBUG)

logger.addHandler(cmdHandler)
