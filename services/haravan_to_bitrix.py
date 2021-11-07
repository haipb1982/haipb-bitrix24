import json
from calendar import mdays
from datetime import datetime, timedelta

from . import bitrix24_service as bx24, bitrix24_service
from dao import deal_dao, product_dao, contact_dao
from utils import log
import migration.deal as Deal
from .mapping_service import convert_object, product_mapping

LOGGER = log.get_logger(__name__)

def create_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
   
    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload})    

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    haravan_order = deal_dao.getHaravanID(haravan_id)

    if haravan_order:
        return False

    fields = Deal.HaravanToBitrix24(payload) 

    # Tạo deal mới trên bitrix
    bitrix24_deal = bitrix24_service.Deal.insert(fields)
    # Lưu dữ liệu từ bitrix vào db để mapping giữa haravan và bitrix
    return deal_dao.addNewDeal(hanravan_id=haravan_id, bitrix24_id=bitrix24_deal.get("ID"), haravan_data=json.dumps(payload),bitrix_data=json.dumps(bitrix24_deal))


def update_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
   
#    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload })

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    haravan_order = deal_dao.getHaravanID(haravan_id)

    if not haravan_order:
        return create_deal_bitrix(payload)

    # TODO: Với trường hợp update thì sẽ cần kiểm tra dữ liệu của webhook data so với dữ liệu trong DB.
    # Nếu khác nhau sẽ cho cập nhật


    
    fields = Deal.HaravanToBitrix24(payload)
    fields["ID"] = haravan_order[2]


    # Tạo deal mới trên bitrix
    result = bitrix24_service.Deal.update(fields)
    if not result:
        return False
    return deal_dao.updateDeal(haravan_id, json.dumps(payload), json.dumps(result))


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
    if not result:
        return False
    return deal_dao.updateDeal(haravan_id, json.dumps(payload), json.dumps(result))


def cancelled_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
        
    LOGGER.info("cancelled_deal_bitrix: ", extra={"payload": payload})
    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    haravan_order = deal_dao.getHaravanID(haravan_id)

    if not haravan_order:
        return create_deal_bitrix(payload)
    
    fields = Deal.HaravanToBitrix24(payload) 
    fields['STAGE_ID'] = "LOSE"
    # Tạo deal mới trên bitrix0
    result = bitrix24_service.Deal.update(fields)
    if not result:
        return False
    return deal_dao.updateDeal(haravan_id, json.dumps(payload), json.dumps(result))


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
    if not result:
        return False
    return deal_dao.updateDeal(haravan_id, json.dumps(payload), json.dumps(result))


def delete_deal_bitrix(id):
    today = datetime.now()
    LOGGER.info("delete_deal_bitrix: ", extra={"today": today})
    haravan_order = deal_dao.getHaravanID(id)
    if not haravan_order or haravan_order[5] == "DELETE":
        return True
    # Tạo deal mới trên bitrix
    bitrix24_service.Deal.delete(haravan_order[2])
    return deal_dao.delete_by_haravan_id(id)

def create_product_bitrix(payload):
    id = payload.get("id")
    haravan_product = product_dao.get_by_haravan_id(id)
    if haravan_product:
        return None, True
    # TODO Cần xử lý product variant trên bitrix
    # variants = payload.get("variants")
    # for variant in variants:
    #     if not variant.get("id"):
    #         continue

    # product = {
    #     "NAME": payload.get("title"),
    #     "DESCRIPTION": payload.get("body_html"),
    #     "PRICE": payload.get("variants")[0].get("price"),
    #     "DATE_CREATE": payload.get("created_at"),
    #     "CURRENCY_ID": "VND",
    # }
    product = convert_object(payload, product_mapping, "BITRIX")
    product["PRICE"] = payload.get("variants")[0].get("price")
    if len(payload.get("images")) > 0:
        product["PREVIEW_PICTURE"] = payload.get("images")[0].get("src")
        product["DETAIL_PICTURE"] = payload.get("images")[0].get("src")
    bitrix24_id = bitrix24_service.Product.insert(fields=product)
    if bitrix24_id:
        product_dao.add_new_product(id, bitrix24_id, "")
        return bitrix24_id, True

    return None, False


def update_product_bitrix(payload):
    id = payload.get("id")
    haravan_product = product_dao.get_by_haravan_id(id)
    if not haravan_product:
        return create_product_bitrix(payload)
    # TODO Cần xử lý product variant trên bitrix
    # variants = payload.get("variants")
    # for variant in variants:
    #     if not variant.get("id"):
    #         continue

    product = {
        "ID": haravan_product[2],
        "NAME": payload.get("title"),
        "DESCRIPTION": payload.get("body_html"),
        "PRICE": payload.get("variants")[0].get("price"),
        "DATE_CREATE": payload.get("created_at"),
        "CURRENCY_ID": "VND",
    }
    if len(payload.get("images")) > 0:
        product["PREVIEW_PICTURE"] = payload.get("images")[0].get("src")
        product["DETAIL_PICTURE"] = payload.get("images")[0].get("src")
    return bitrix24_service.Product.update(product)

def deleted_product_bitrix(id):
    haravan_product = product_dao.get_by_haravan_id(id)
    if haravan_product:
        bitrix24_id = bitrix24_service.Product.delete(haravan_product[2])
        if bitrix24_id:
            product_dao.delete_by_haravan_id(id)
    return None, True

def create_contact_bitrix(payload):
    id = payload.get("id")
    haravan_contact = contact_dao.get_by_haravan_id(id)
    if haravan_contact:
        return None, True
    contact = {
        "NAME": payload.get("default_address").get("name"),
        "SECOND_NAME": payload.get("default_address").get("first_name"),
        "LAST_NAME": payload.get("default_address").get("last_name"),
        "ADDRESS": payload.get("default_address").get("address1"),
        "ADDRESS_CITY": payload.get("default_address").get("city"),
        "ADDRESS_POSTAL_CODE": payload.get("default_address").get("zip"),
        "ADDRESS_COUNTRY": payload.get("default_address").get("country"),
        "PHONE": [ { "VALUE": payload.get("default_address").get("phone"), "VALUE_TYPE": "WORK" } ],
        "TYPE_ID": "CLIENT",
        "ADDRESS_PROVINCE": payload.get("default_address").get("province"),
        "OPENED": "Y",
    }
    bitrix24_id = bitrix24_service.Contact.insert(fields=contact)
    if bitrix24_id:
        contact_dao.add_new_contact(id, bitrix24_id, json.dumps(payload), None)
        return bitrix24_id, True

    return None, False

def update_contact_bitrix(payload):
    id = payload.get("id")
    haravan_contact = contact_dao.get_by_haravan_id(id)
    if not haravan_contact:
        return create_contact_bitrix(payload)
    contact = {
        "ID": haravan_contact[2],
        "NAME": payload.get("default_address").get("name"),
        "SECOND_NAME": payload.get("default_address").get("first_name"),
        "LAST_NAME": payload.get("default_address").get("last_name"),
        "ADDRESS": payload.get("default_address").get("address1"),
        "ADDRESS_CITY": payload.get("default_address").get("city"),
        "ADDRESS_POSTAL_CODE": payload.get("default_address").get("zip"),
        "ADDRESS_COUNTRY": payload.get("default_address").get("country"),
        "PHONE": [ { "VALUE": payload.get("default_address").get("phone"), "VALUE_TYPE": "WORK" } ],
        "TYPE_ID": "CLIENT",
        "ADDRESS_PROVINCE": payload.get("default_address").get("province"),
        "OPENED": "Y",
    }
    bitrix24_id = bitrix24_service.Contact.update(contact)
    if bitrix24_id:
        return bitrix24_id, True
    
    return None, False

def delete_contact_bitrix(id):
    haravan_contact = contact_dao.get_by_haravan_id(id)
    if haravan_contact:
        bitrix24_id = bitrix24_service.Contact.delete(haravan_contact[2])
        if bitrix24_id:
            contact_dao.delete_by_haravan_id(id)
    return None, True