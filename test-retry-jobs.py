import time
from services import retryjob_service

while True:
    # Code executed here
    print('tick!')
    retryjob_service.retry_all_jobs()
    time.sleep(15*60)

