from .mapping_service import convert_object, product_mapping, contact_mapping
from utils import log, common
import json

from mysqldb.dao.RetryJobDAO import RetryJobDAO
from services import haravan_to_bitrix ,bitrix_to_haravan, webapp_service

retryJob_dao = RetryJobDAO()

LOGGER = log.get_logger(__name__)

JOB_RETRY_TIME_LIMIT = 10

# thêm mới job vào table tbl_retry_job
def insert(haravan_id=None, haravan_data=None, bitrix24_id=None, bitrix_data=None , type=None, action=None):
    if type=='ORDERS' or type=='ORDER':
        common.addRowCSV([haravan_id],'retry_orders.csv')
    return retryJob_dao.insertRetryJobRecord(haravan_id, bitrix24_id, json.dumps(haravan_data), json.dumps(bitrix_data), type, action)

def getAll():
    return retryJob_dao.getAllRetryJobRecords()

def getOrders():
    return retryJob_dao.getOrderRetryJobRecords()

def haravan_migrate(job_data):
    
    type =  job_data.get('type')
    action =  job_data.get('action')
    haravan_id = job_data.get('haravan_id')
    payload = json.loads(job_data.get('haravan_data'))

    print('retry jobs : haravan_migrate',haravan_id, type, action)
    result = False
    
    if type == 'ORDERS':
        if action == 'CREATE':
            result = haravan_to_bitrix.create_deal_bitrix(payload)
        if action == 'UPDATED':
            result = haravan_to_bitrix.update_deal_bitrix(payload)
        if action == 'PAID':
            result = haravan_to_bitrix.paid_deal_bitrix(payload)
        if action =='CANCELLED':
            result = haravan_to_bitrix.cancelled_deal_bitrix(payload)
        if action =='FULFILLED':
            result = haravan_to_bitrix.fulfilled_deal_bitrix(payload)
        if action =='DELETE':
            result = haravan_to_bitrix.delete_deal_bitrix(haravan_id)
            

    if type == 'CUSTOMERS':
        if action == 'CREATE':
            result = haravan_to_bitrix.create_contact_bitrix(payload)
        if action == 'UPDATE':
            result = haravan_to_bitrix.update_contact_bitrix(payload)
        if action =='DELETE':
            result = haravan_to_bitrix.delete_contact_bitrix(haravan_id)

    if type == 'PRODUCTS':
        if action == 'CREATE':
            result = haravan_to_bitrix.create_product_bitrix(payload)
        if action == 'UPDATE':
            result = haravan_to_bitrix.update_product_bitrix(payload)
        if action =='DELETE':
            result = haravan_to_bitrix.deleted_product_bitrix(haravan_id)
    
    print(result)
    return result

def bx24_migrate(job_data):

    type =  job_data.get('type')
    action =  job_data.get('action')
    bitrix24ID = job_data.get('bitrix24_id')

    result = False

    if type == "ONCRMDEALADD":
        result = bitrix_to_haravan.create_order_haravan(bitrix24ID)
    if type == "ONCRMDEALUPDATE":
        result = bitrix_to_haravan.update_order_haravan(bitrix24ID)
    if type == "ONCRMPRODUCTDELETE":
        result = bitrix_to_haravan.delete_order_haravan(bitrix24ID)

    if type == "ONCRMPRODUCTADD":
        result = bitrix_to_haravan.create_product_haravan(bitrix24ID)
    if type == "ONCRMPRODUCTUPDATE":
        result = bitrix_to_haravan.update_product_haravan(bitrix24ID)
    if type == "ONCRMPRODUCTDELETE":
        result = bitrix_to_haravan.delete_product_haravan(bitrix24ID)

    if type == "ONCRMCONTACTADD":
        result = bitrix_to_haravan.create_contact_haravan(bitrix24ID)
    if type == "ONCRMCONTACTUPDATE":
        result = bitrix_to_haravan.update_contact_haravan(bitrix24ID)
    if type == "ONCRMCONTACTDELETE":
        result = bitrix_to_haravan.delete_contact_haravan(bitrix24ID)
    
    return result

# chạy lại các job trong table tbl_retry_job cho đến retry count nhỏ hơn JOB_RETRY_TIME_LIMIT (10 lần)
def retry_all_jobs():
    
    retryJob_dao.updateRetryTime() # all retry_time++ nếu vượt quá JOB_RETRY_TIME_LIMIT sẽ không retry nữa

    list_retry_jobs = retryJob_dao.getAllRetryJobRecords(JOB_RETRY_TIME_LIMIT)
    
    if list_retry_jobs.get('code') == 500:
        return

    for job in list_retry_jobs.get('data'):
        result = False
        if job.get('haravan_id'):
            print('haravan migrate', job.get('haravan_id'),job.get('type'),job.get('action'))
            result = haravan_migrate(job)

        if job.get('bitrix24_id'):
            print('bitrix24 migrate', job.get('bitrix24_id'),job.get('type'),job.get('action'))
            result = bx24_migrate(job)

        if result:
            retryJob_dao.deleteRetryJobRecord(job.get('id'))

def retry_orders():
    orders = common.readCSV('retry_orders.csv')
    for order in orders:
        if order[0]:
            res = webapp_service.get_sync('orders',order[0])
            # print(res['data'])
            if res['data']:
                # print('OK retry!!!')
                common.removeRowCSV(order[0],'retry_orders.csv')
