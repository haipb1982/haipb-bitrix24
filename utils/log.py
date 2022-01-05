import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            log_record['timestamp'] = now

        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
            if log_record['level'] == 'WARNING':
                log_record['level'] = '\033[93m' + log_record['level'] + '\033[0m'
        else:
            log_record['level'] = record.levelname

        # if log_record.get('message'):
        #     s = log_record['message']
        #     log_record['message'] = s.decode('utf-8')    


def get_logger(name: str) -> logging.Logger:
    """Returns the central logger."""

    # Create a custom logger
    logger = logging.getLogger(name)

    # # Setup logger level
    # logger.setLevel(env.LOGLEVEL)

    # Setup logger custom handler
    handler = logging.StreamHandler()

    formatter = CustomJsonFormatter('%(level)s - %(timestamp)s : %(name)s %(message)s')
    # formatter = CustomJsonFormatter()

    handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(handler)

    return logger


def _init_module():
    # Change the root level to lowest
    logging.getLogger().setLevel(logging.DEBUG)


_init_module()
