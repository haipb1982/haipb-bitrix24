from calendar import mdays
from datetime import datetime, timedelta

from . import bitrix24_service as bx24, bitrix24_service
from dao import deal_dao, product_dao
from utils import log
import migration.deal as Deal

LOGGER = log.get_logger(__name__)

def create_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
   
    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload})    

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    haravan_order = deal_dao.getHaravanID(haravan_id)

    if haravan_order:
        return None, False
    fields = Deal.HaravanToBitrix24(payload) 

    # Tạo deal mới trên bitrix
    bitrix24_id = bitrix24_service.Deal.insert(fields)
    # Lưu dữ liệu từ bitrix vào db để mapping giữa haravan và bitrix
    result = deal_dao.addNewDeal(hanravan_id=id, bitrix24_id=bitrix24_id, note="")
    return result, True


def update_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
   
#    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload })

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    haravan_order = deal_dao.getHaravanID(haravan_id)

    if not haravan_order:
        return create_deal_bitrix(payload)
    
    fields = Deal.HaravanToBitrix24(payload) 

    # Tạo deal mới trên bitrix
    result = bitrix24_service.Deal.update(fields)
    return result, True


def paid_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
        
    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload})

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    haravan_order = deal_dao.getHaravanID(haravan_id)

    if not haravan_order:
        return create_deal_bitrix(payload)
    
    fields = Deal.HaravanToBitrix24(payload) 
    fields['STAGE_ID'] = "FINAL_INVOICE"
    # Tạo deal mới trên bitrix
    result = bitrix24_service.Deal.update(fields)
    return result, True


def cancelled_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
        
    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload})
    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    haravan_order = deal_dao.getHaravanID(haravan_id)

    if not haravan_order:
        return create_deal_bitrix(payload)
    
    fields = Deal.HaravanToBitrix24(payload) 
    fields['STAGE_ID'] = "LOSE"
    # Tạo deal mới trên bitrix0
    result = bitrix24_service.Deal.update(fields)
    return result, True


def fulfilled_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
        
    LOGGER.info("fulfilled_deal_bitrix: ", extra={"payload": payload})
    
    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    haravan_order = deal_dao.getHaravanID(haravan_id)

    if not haravan_order:
        return create_deal_bitrix(payload)
    
    fields = Deal.HaravanToBitrix24(payload) 
    fields['STAGE_ID'] = "WON"
    # Tạo deal mới trên bitrix
    result = bitrix24_service.Deal.update(fields)
    return result, True


def delete_deal_bitrix(id):
    today = datetime.now()
    LOGGER.info("delete_deal_bitrix: ", extra={"today": today})
    haravan_order = deal_dao.getHaravanID(id)
    if not haravan_order:
        return None, True
    # Tạo deal mới trên bitrix
    result = bitrix24_service.Deal.delete(haravan_order[2])
    deal_dao.deleteHaravanID(id)
    return result, True

def create_product_bitrix(payload):
    id = payload.get("id")
    haravan_product = product_dao.get_by_haravan_id(id)
    if haravan_product:
        return None, True

    pass

def update_product_bitrix():
    pass

def deleted_product_bitrix():
    pass