import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

from . import env

# minimize boto3 loggging
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().isoformat()
            log_record['timestamp'] = now

        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


def get_logger(name: str) -> logging.Logger:
    """Returns the central logger."""

    # Create a custom logger
    logger = logging.getLogger(name)

    # Setup logger level
    logger.setLevel(env.LOGLEVEL)

    # Setup logger custom handler
    handler = logging.StreamHandler()
    handler.setFormatter(CustomJsonFormatter())
    logger.handlers.clear()
    logger.addHandler(handler)

    return logger


def _init_module():
    # Change the root level to lowest
    logging.getLogger().setLevel(logging.DEBUG)


_init_module()
