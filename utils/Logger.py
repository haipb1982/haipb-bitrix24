import os
import logging 
# import settings   # alternativly from whereever import settings  

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
class myFormatter(logging.Formatter):
    def format(self, record):
        if 'extra' not in dir(record):
            # print('Got extra:', record.extra) # or do whatever you want with _extra
            record.extra = None
        # color log
        if record.levelname == 'INFO':
            record.levelname = bcolors.OKCYAN + record.levelname + bcolors.ENDC
        if record.levelname == 'ERROR':
            record.levelname = bcolors.FAIL + record.levelname + bcolors.ENDC
        if record.levelname == 'WARNING' or record.levelname == 'WARN':
            record.levelname = bcolors.WARNING + record.levelname + bcolors.ENDC

        return super().format(record)

class ExtraLogFormatter(logging.Formatter):                                                                             
    def format(self, record):                                                                                           
        dummy = logging.LogRecord(None,None,None,None,None,None,None)                                                   
        extra_txt = ''                                                                                                  
        for k,v in record.__dict__.items():                                                                             
            if k not in dummy.__dict__:                                                                                 
                extra_txt += ', {}={}'.format(k,v)                                                                      
        message = super().format(record)                                                                                
        return message + extra_txt 
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
            # formatter = ExtraLogFormatter('*** %(levelname)s | %(asctime)s | %(name)s %(message)s -extra- %(extra)s')
            formatter =myFormatter('*** %(levelname)s | %(asctime)s | %(name)s | %(message)s | %(extra)s')

            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            
            logger.addHandler(handler)
            
        self._logger = logger

    def get(self):
        return self._logger