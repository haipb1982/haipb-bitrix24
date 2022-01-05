import logging

def make_record_with_extra(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
    record = original_makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
    record._extra = extra
    return record

original_makeRecord = logging.Logger.makeRecord
logging.Logger.makeRecord = make_record_with_extra

class myFormatter(logging.Formatter):
    def format(self, record):
        print('Got extra:', record._extra)
        return super().format(record)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(myFormatter('%(name)s - %(levelname)s - %(message)s - %(foo)s'))
logger.addHandler(handler)
logger.warning('test', extra={'foo': 'bar'})