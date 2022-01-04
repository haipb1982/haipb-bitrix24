import os
import logging 
# import settings   # alternativly from whereever import settings  

class myFormatter(logging.Formatter):
    def format(self, record):
        print('Got extra:', record._extra) # or do whatever you want with _extra
        return super().format(record)
class Logger(object):

    def __init__(self, name):
        name = name.replace('.log','')
        logger = logging.getLogger('BLU.%s' % name)    # log_namespace can be replaced with your namespace 
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            # file_name = os.path.join(settings.LOGGING_DIR, '%s.log' % name)    # usually I keep the LOGGING_DIR defined in some global settings file
            # file_name = os.path.join("logs", '%s.log' % name)
            # handler = logging.FileHandler(file_name)
            handler = logging.StreamHandler()
            # formatter = logging.Formatter('%(levelname)s - %(asctime)s : %(name)s %(message)s')
            # handler.setFormatter(formatter)
            # handler.LoggerAdapter(logger, extra)
            handler.setFormatter(myFormatter('%(levelname)s - %(asctime)s : %(name)s %(message)s - %(foo)s'))
            handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)

        self._logger = logger

    def get(self):
        return self._logger