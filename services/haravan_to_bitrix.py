import json
from calendar import mdays
from datetime import datetime, timedelta

from . import bitrix24_service as bx24, bitrix24_service, mapping_service
# from dao import deal_dao, product_dao, contact_dao
from mysqldb.dao.DealDAO import DealDAO 
from mysqldb.dao.ProductDAO import ProductDAO
from mysqldb.dao.ContactDAO import ContactDAO

deal_dao = DealDAO()
product_dao = ProductDAO()
contact_dao = ContactDAO()

from utils import log
import migration.deal as Deal
from .mapping_service import convert_object, product_mapping, contact_mapping

LOGGER = log.get_logger(__name__)

def create_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
   
    # LOGGER.info("create_deal_bitrix: ", extra={"payload": payload})    

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    deal_order = deal_dao.getDataByHaID(haravan_id)

    if deal_order:
        print('HaravanID đã tồn tại trong database')
        return False
    fields = Deal.HaravanToBitrix24(payload) 

    # Tạo deal mới trên bitrix
    bitrix24_deal = bitrix24_service.Deal.insert(fields)
    # Lưu dữ liệu từ bitrix vào db để mapping giữa haravan và bitrix
    return deal_dao.addNewDeal(
        hanravan_id=haravan_id,
        bitrix24_id=bitrix24_deal.get("ID"),
        haravan_data=json.dumps(payload),
        bitrix_data=json.dumps(bitrix24_deal)
    )


def update_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
   
#    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload })

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    deal_order = deal_dao.getDataByHaID(haravan_id)

    if not deal_order:
        print('HaravanID chưa có trong database! Đang tạo mới Deal trên Bitrix24')
        return create_deal_bitrix(payload)

    # TODO: Với trường hợp update thì sẽ cần kiểm tra dữ liệu của webhook data so với dữ liệu trong DB.
    # Nếu khác nhau sẽ cho cập nhật

    if Deal.CompareHaravanNewData(deal_order, payload):
        print('No data changed! Không có thay đổi dữ liệu tbl_deal_order')
        return None

    # # #
    
    fields = Deal.HaravanToBitrix24(payload)
    fields["ID"] = deal_order[0].get('bitrix24_id')


    # Cập nhật deal trên bitrix
    result = bitrix24_service.Deal.update(fields)

    return deal_dao.updateDeal(haravan_id, json.dumps(payload), json.dumps(result))


def paid_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
        
    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload})

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    deal_order = deal_dao.getDataByHaID(haravan_id)

    if not deal_order:
        print('HaravanID chưa có trong database! Đang tạo mới Deal trên Bitrix24')
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
    deal_order = deal_dao.getDataByHaID(haravan_id)

    if not deal_order:
        print('HaravanID chưa có trong database! Đang tạo mới Deal trên Bitrix24')
        return create_deal_bitrix(payload)
    
    fields = Deal.HaravanToBitrix24(payload) 
    fields['STAGE_ID'] = "LOSE"
    # Tạo deal mới trên bitrix0
    result = bitrix24_service.Deal.update(fields)
    if not result:
        print('Cập nhật Deal trên Bitrix24 thất bại!')
        return False
    return deal_dao.updateDeal(haravan_id, json.dumps(payload), json.dumps(result))


def fulfilled_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
        
    LOGGER.info("fulfilled_deal_bitrix: ", extra={"payload": payload})
    
    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    deal_order = deal_dao.getDataByHaID(haravan_id)

    if not deal_order:
        print('HaravanID chưa có trong database! Đang tạo mới Deal trên Bitrix24')
        return create_deal_bitrix(payload)
    
    fields = Deal.HaravanToBitrix24(payload) 
    fields['STAGE_ID'] = "WON"
    # Tạo deal mới trên bitrix
    result = bitrix24_service.Deal.update(fields)
    if not result:
        print('Cập nhật Deal trên Bitrix24 thất bại!')
        return False
    return deal_dao.updateDeal(haravan_id, json.dumps(payload), json.dumps(result))


def delete_deal_bitrix(id):
    today = datetime.now()
    # LOGGER.info("delete_deal_bitrix: ", extra={"today": today})
    deal_order = deal_dao.getDataByHaID(id)
    if not deal_order or deal_order[0].get('status') == "DELETE":
        print('Bản ghi tbl_deal_order không tìm thấy!')
        return True
    # Xoá deal trên bitrix
    bitrix24_service.Deal.delete(deal_order[0].get('bitrix24_id'))
    return deal_dao.delete_by_haravan_id(id)

def create_product_bitrix(payload):
    id = payload.get("id")
    haravan_product = product_dao.get_by_haravan_id(id)
    if haravan_product or (haravan_product and (haravan_product.get('haravan_data').get('status') == "DELETE")):
        return None
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

    bitrix24_data = bitrix24_service.Product.insert(fields=product)
    if bitrix24_data:
        product_dao.add_new_product(id, bitrix24_data.get("ID"), json.dumps(payload), json.dumps(bitrix24_data))
        return bitrix24_data.get("ID")

    return None


def update_product_bitrix(payload):
    id = payload.get("id")
    haravan_product = product_dao.get_by_haravan_id(id)

    if not haravan_product:
        return None

    bitrix24_id = haravan_product.get("bitrix24_id")

    old_data = json.loads(haravan_product.get('haravan_data'))
    new_data = payload
    changed_data = mapping_service.get_changed_data(old_data, new_data)

    # Nếu data ko có gì sẽ thay đổi thì sẽ ko cần cập nhật vào haravan nữa tránh tình trạng bị trigger vòng tròn
    if not changed_data:
        return

    # TODO Cần xử lý product variant trên bitrix
    # variants = payload.get("variants")
    # for variant in variants:
    #     if not variant.get("id"):
    #         continue

    data_update = mapping_service.convert_object(changed_data, product_mapping, "BITRIX")
    data_update["ID"] = bitrix24_id

    bitrix_data = bitrix24_service.Product.update(data_update)
    if bitrix_data:
        return product_dao.update_by_haravan_id(id, haravan_data=json.dumps(new_data), bitrix_data=json.dumps(bitrix_data))
    return None

def deleted_product_bitrix(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    haravan_product = product_dao.get_by_haravan_id(id)

    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if not haravan_product or haravan_product.get("haravan_status") == "DELETE" and haravan_product.get("bitrix_status") == "DELETE":
        return None

    # Xóa dữ liệu được trigger từ bitrix trong DB -> Đánh dấu là DELETE
    product_dao.delete_by_haravan_id(id)
    bitrix24_id = haravan_product.get("bitrix24_id")
    result = bitrix24_service.Product.delete(bitrix24_id)
    if result:
        product_dao.delete_by_bitrix_id(bitrix24_id)
        return result
    return None

def create_contact_bitrix(payload):
    id = payload.get("id")
    haravan_contact = contact_dao.get_by_haravan_id(id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if haravan_contact:
        print('HaravanID đã có trong database! Tạo mới thất bại!')
        return None
    if (haravan_contact and (haravan_contact.get("haravan_status") == "DELETE" and haravan_contact.get("bitrix_status") == "DELETE")):
        print('HaravanID đã tồn tại trong database! Tạo mới thất bại!')
        return None
    # contact = {
    #     "NAME": payload.get("default_address").get("name"),
    #     "SECOND_NAME": payload.get("default_address").get("first_name"),
    #     "LAST_NAME": payload.get("default_address").get("last_name"),
    #     "ADDRESS": payload.get("default_address").get("address1"),
    #     "ADDRESS_CITY": payload.get("default_address").get("city"),
    #     "ADDRESS_POSTAL_CODE": payload.get("default_address").get("zip"),
    #     "ADDRESS_COUNTRY": payload.get("default_address").get("country"),
    #     "PHONE": [ { "VALUE": payload.get("default_address").get("phone"), "VALUE_TYPE": "WORK" } ],
    #     "TYPE_ID": "CLIENT",
    #     "ADDRESS_PROVINCE": payload.get("default_address").get("province"),
    #     "OPENED": "Y",
    # }

    contact = mapping_service.convert_object(payload, contact_mapping, "BITRIX")

    bitrix24_data = bitrix24_service.Contact.insert(fields=contact)
    if bitrix24_data:
        contact_dao.add_new_contact(id, bitrix24_data.get("ID"), json.dumps(payload), json.dumps(bitrix24_data))
        print('Tạo mới Contact Bitrix24 thành công!')
        return bitrix24_data

    return None

def update_contact_bitrix(payload):
    haravan_id = payload.get("id")
    haravan_contact = contact_dao.get_by_haravan_id(haravan_id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if not haravan_contact or haravan_contact.get("haravan_status") == "DELETE" and haravan_contact.get("bitrix_status") == "DELETE":
        return None

    if not haravan_contact:
        return None
    # contact = {
    #     "ID": haravan_contact[2],
    #     "NAME": payload.get("default_address").get("name"),
    #     "SECOND_NAME": payload.get("default_address").get("first_name"),
    #     "LAST_NAME": payload.get("default_address").get("last_name"),
    #     "ADDRESS": payload.get("default_address").get("address1"),
    #     "ADDRESS_CITY": payload.get("default_address").get("city"),
    #     "ADDRESS_POSTAL_CODE": payload.get("default_address").get("zip"),
    #     "ADDRESS_COUNTRY": payload.get("default_address").get("country"),
    #     "PHONE": [ { "VALUE": payload.get("default_address").get("phone"), "VALUE_TYPE": "WORK" } ],
    #     "TYPE_ID": "CLIENT",
    #     "ADDRESS_PROVINCE": payload.get("default_address").get("province"),
    #     "OPENED": "Y",
    # }

    old_data = json.loads(haravan_contact.get("haravan_data"))

    new_data = payload
    changed_data = mapping_service.get_changed_data(old_data, new_data)

    # Nếu data ko có gì sẽ thay đổi thì sẽ ko cần cập nhật vào haravan nữa tránh tình trạng bị trigger vòng tròn
    if not changed_data:
        return

    bitrix_id = haravan_contact.get("bitrix24_id")
    contact = mapping_service.convert_object(changed_data, contact_mapping, "BITRIX")
    contact["ID"] = bitrix_id

    bitrix24_data = bitrix24_service.Contact.update(contact)
    # Xử lý nếu data haravan trả về đúng
    if bitrix24_data:
        return contact_dao.update_by_haravan_id(haravan_id, haravan_data=json.dumps(new_data),
                                                bitrix_data=json.dumps(bitrix24_data))
    else:
        return None


def delete_contact_bitrix(id):

    haravan_contact = contact_dao.get_by_haravan_id(id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if not haravan_contact or haravan_contact.get("haravan_status") == "DELETE" and haravan_contact("bitrix_status") == "DELETE":
        return False

    # Xóa dữ liệu được trigger từ bitrix trong DB -> Đánh dấu là DELETE
    contact_dao.delete_by_haravan_id(id)

    bitrix24_id = haravan_contact.get("bitrix24_id")

    result = bitrix24_service.Contact.delete(bitrix24_id)
    if result:
        contact_dao.delete_by_bitrix_id(bitrix24_id)
        return True
    return False

def testCon():
    print(deal_dao.getAllDeals())
    # print(contact_dao.getAllContacts())
    # print(product_dao.getAllProducts())