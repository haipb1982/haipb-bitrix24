import json
from calendar import mdays
from datetime import datetime, timedelta

from . import bitrix24_service as bx24, bitrix24_service, mapping_service, haravan_service
# from dao import deal_dao, product_dao, contact_dao
from mysqldb.dao.DealDAO import DealDAO
from mysqldb.dao.ProductDAO import ProductDAO
from mysqldb.dao.ContactDAO import ContactDAO
from .bitrix24_service import DealProductRow

deal_dao = DealDAO()
product_dao = ProductDAO()
contact_dao = ContactDAO()

from utils import log, common
import migration.deal as Deal
from .mapping_service import convert_object, product_mapping, contact_mapping

LOGGER = log.get_logger(__name__)

def create_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
        return False

    # LOGGER.info("create_deal_bitrix: ", extra={"payload": payload})    

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id",None)
    deal_order = deal_dao.getDealOrderByHaID(haravan_id)

    if deal_order.get('data',None):
        print('HaravanID đã tồn tại trong database')
        return False

    # Lấy thông tin customer từ khách hàng để set cho CONTACT_ID. Nếu không có sẽ tạo mới customer
    customer = payload.get("customer")
    customer_id = customer.get("id",None)
    if customer_id:
        customer_contact_result = contact_dao.get_by_haravan_id(customer_id)
    if customer_contact_result:
        contact_bitrix_id = customer_contact_result.get("bitrix24_id")
    else:
        contact_bitrix = create_contact_bitrix(customer)
        contact_bitrix_id = contact_bitrix.get("ID")


    fields = Deal.HaravanToBitrix24(payload)
    fields["CONTACT_ID"] = contact_bitrix_id

    # lấy thông tin người tạo từ haravan để gán cho bitrix
    user_id = payload.get("user_id")
    print('người tạo đơn',user_id)
    haravan_user = haravan_service.User.get(user_id)
    print('người tạo đơn',haravan_user)
    if haravan_user and haravan_user.get("user"):
        user = haravan_user.get("user")
        print('người tạo đơn',user)
        fields['UF_CRM_1630417157521'] = user.get("last_name", "") + " " + user.get("first_name", "")
    else:
        fields['UF_CRM_1630417157521'] = 'HARAVAN-BITRIX24 APP' # người tạo đơn
    # fields["STAGE_ID"] = "C18:NEW"
    # fields["UF_CRM_1637252157269"] = str(payload.get("id"))

    # Tạo deal mới trên bitrix 
    
    bitrix24_deal = bitrix24_service.Deal.insert(fields)
    if not bitrix24_deal.get("ID"):
        print('Không tạo được Bitrix24 Deal mới!')
        return False
        
    add_result = deal_dao.addNewDeal(
        hanravan_id=haravan_id,
        bitrix24_id=bitrix24_deal.get("ID"),
        haravan_data=json.dumps(payload),
        bitrix_data=json.dumps(bitrix24_deal)
    )
    # Nếu không thành công thì chỉ add id và chạy update lại
    if add_result:
        deal_dao.addNewDeal(
        hanravan_id=haravan_id,
        bitrix24_id=bitrix24_deal.get("ID"),
        haravan_data=None,
        bitrix_data=None
        )
        update_deal_bitrix_all(topic='orders/updated', payload=payload)
    
    product_haravans = payload.get("line_items",None)

    productrows = {}
    i = 0
    for product_haravan in product_haravans:
        productrow = {}
        product_result = product_dao.get_by_haravan_id(product_haravan.get("id",None))
        if product_result:
            product_id = product_result.get("bitrix24_id")
        else:
            product = haravan_service.Product.get(product_haravan.get("id",None))
            product_bitrix = create_product_bitrix(product)
            product_id = product_bitrix.get("ID")
        productrow["PRODUCT_ID"] = product_id
        productrow["PRICE"] = product_haravan.get("price",0)
        productrow["QUANTITY"] = product_haravan.get("quantity",0)

        productrow["PRODUCT_NAME"] = product_haravan.get("name",None) or product_haravan.get("title",None)
        
        if product_haravan.get("image",None):
            fileData = product_haravan["image"].get("src","https://vnztech.com/no-image.png")
        else:
            fileData = "https://vnztech.com/no-image.png"
        # productrow["PREVIEW_PICTURE"] = {'fileData':[fileData]}
        # productrow["DETAIL_PICTURE"] = {'fileData':[fileData]}
        productrow["PREVIEW_PICTURE"] = [fileData,fileData]
        productrow["DETAIL_PICTURE"] = [fileData,fileData]

        productrow["DISCOUNT_TYPE_ID"] = 1 
        productrow["DISCOUNT_SUM"] = product_haravan.get("total_discount",0)

        productrows[i] = productrow
        i = i + 1

    # Add product vào trong DEAL

    fields = {
        "id": bitrix24_deal.get("ID"),
        "rows": productrows
    }

    # print('DealProductRow',fields)
    deal_productrow = DealProductRow.set(fields)

    # Lưu dữ liệu từ bitrix vào db để mapping giữa haravan và bitrix
    return deal_productrow


def update_deal_bitrix(payload=None):
    if payload is None:
        payload = {}

    #    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload })

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    deal_order = deal_dao.getDealOrderByHaID(haravan_id)

    if not deal_order.get('data',None):
        print('HaravanID chưa có trong database! Đang tạo mới Deal trên Bitrix24')
        return create_deal_bitrix(payload)

    # TODO: Với trường hợp update thì sẽ cần kiểm tra dữ liệu của webhook data so với dữ liệu trong DB.
    # Nếu khác nhau sẽ cho cập nhật

    if Deal.CompareHaravanNewData(deal_order['data'][0], payload):
        print('No data changed! Không có thay đổi dữ liệu tbl_deal_order')
        return None


    fields = Deal.HaravanToBitrix24(payload)
    fields["ID"] = deal_order['data'][0].get('bitrix24_id')


    # Cập nhật deal trên bitrix
    result = bitrix24_service.Deal.update(fields)

    # Cập nhật products của Deal 
    product_haravans = payload.get("line_items", None)

    productrows = {}
    i = 0
    for product_haravan in product_haravans:
        productrow = {}
        product_result = product_dao.get_by_haravan_id(product_haravan.get("id",None))
        if product_result:
            product_id = product_result.get("bitrix24_id")
        else:
            product = haravan_service.Product.get(product_haravan.get("id",None))
            product_bitrix = create_product_bitrix(product)
            product_id = product_bitrix.get("ID")
        productrow["PRODUCT_ID"] = product_id
        productrow["PRICE"] = product_haravan.get("price",0)
        productrow["QUANTITY"] = product_haravan.get("quantity",0)

        productrow["PRODUCT_NAME"] = product_haravan.get("name",None) or product_haravan.get("title",None)
        
        if product_haravan.get("image",None):
            fileData = product_haravan["image"].get("src","https://vnztech.com/no-image.png")
        else:
            fileData = "https://vnztech.com/no-image.png"
        productrow["PREVIEW_PICTURE"] = [{'fileData':fileData}]
        productrow["DETAIL_PICTURE"] = [{'fileData':fileData}]
        # productrow["PREVIEW_PICTURE"] = fileData
        # productrow["DETAIL_PICTURE"] = fileData

        productrow["DISCOUNT_TYPE_ID"] = 1 
        productrow["DISCOUNT_SUM"] = product_haravan.get("total_discount",0)

        productrows[i] = productrow
        i = i + 1

    # Add products vào trong DEAL

    fields = {
        "id": fields["ID"],
        "rows": productrows
    }
    
    deal_productrow = DealProductRow.set(fields)
    print('DealProductRow',deal_productrow)

    return deal_dao.updateDeal(haravan_id, json.dumps(payload), json.dumps(result))

def update_deal_bitrix_all(topic='', payload=None):
    if payload is None:
        payload = {}

    #    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload })

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    deal_order = deal_dao.getDealOrderByHaID(haravan_id)

    # print('update_deal_bitrix_all',deal_order)

    if not deal_order.get('data',None):
        print('HaravanID chưa có trong database! Đang tạo mới Deal trên Bitrix24')
        return create_deal_bitrix(payload)
    else:
        print('HaravanID có trong database!')

    # TODO: Với trường hợp update thì sẽ cần kiểm tra dữ liệu của webhook data so với dữ liệu trong DB.
    # Nếu khác nhau sẽ cho cập nhật

    if Deal.CompareHaravanNewData(deal_order["data"][0], payload):
        print('No data changed! Không có thay đổi dữ liệu tbl_deal_order')
        return None
    else:
        print('Data changed! continue updating...')


    fields = Deal.HaravanToBitrix24(payload)
    fields["ID"] = deal_order['data'][0].get('bitrix24_id')
    # if topic in ['orders/updated']:
    #     fields['STAGE_ID'] = "C18:NEW"
    if topic in ['orders/paid']:
        fields['STAGE_ID'] = "C18:FINAL_INVOICE"
    if topic in ['orders/cancelled']:
        fields['STAGE_ID'] = "C18:LOSE"
    if topic in ['orders/fulfilled']:
        fields['STAGE_ID'] = "C18:WON"
    

    # Cập nhật deal trên bitrix
    result = bitrix24_service.Deal.update(fields)
    print('Cập nhật trên bitrix',result)

    # Cập nhật products của Deal 
    product_haravans = payload.get("line_items")

    productrows = {}
    i = 0
    for product_haravan in product_haravans:
        productrow = {}
        product_result = product_dao.get_by_haravan_id(product_haravan.get("id"))
        if product_result:
            product_id = product_result.get("bitrix24_id")
        else:
            product = haravan_service.Product.get(product_haravan.get("id"))
            product_bitrix = create_product_bitrix(product)
            product_id = product_bitrix.get("ID")
        productrow["PRODUCT_ID"] = product_id
        productrow["PRICE"] = product_haravan.get("price",0)
        productrow["QUANTITY"] = product_haravan.get("quantity",0)

        productrow["PRODUCT_NAME"] = product_haravan.get("name",None) or product_haravan.get("title",None)
        
        if product_haravan.get("image"):
            fileData = product_haravan["image"].get("src","https://vnztech.com/no-image.png")
        else:
            fileData = "https://vnztech.com/no-image.png"
        productrow["PREVIEW_PICTURE"] = [{'fileData':fileData}]
        productrow["DETAIL_PICTURE"] = [{'fileData':fileData}]
        # productrow["PREVIEW_PICTURE"] = fileData
        # productrow["DETAIL_PICTURE"] = fileData

        productrow["DISCOUNT_TYPE_ID"] = 1 
        productrow["DISCOUNT_SUM"] = product_haravan.get("total_discount",0)

        productrows[i] = productrow
        i = i + 1

    # Add products vào trong DEAL

    fields = {
        "id": fields["ID"],
        "rows": productrows
    }
    
    deal_productrow = DealProductRow.set(fields)
    # print('DealProductRow',deal_productrow)

    return deal_dao.updateDeal(haravan_id, json.dumps(payload), json.dumps(result))

def paid_deal_bitrix(payload=None):
    if payload is None:
        payload = {}

    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload})

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    deal_order = deal_dao.getDealOrderByHaID(haravan_id)

    if not deal_order.get('data',None):
        print('HaravanID chưa có trong database! Đang tạo mới Deal trên Bitrix24')
        return create_deal_bitrix(payload)

    fields = Deal.HaravanToBitrix24(payload)
    fields['STAGE_ID'] = "C18:FINAL_INVOICE"
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
    deal_order = deal_dao.getDealOrderByHaID(haravan_id)

    if not deal_order.get('data',None):
        print('HaravanID chưa có trong database! Đang tạo mới Deal trên Bitrix24')
        return create_deal_bitrix(payload)

    fields = Deal.HaravanToBitrix24(payload)
    fields['STAGE_ID'] = "C18:LOSE"
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
    deal_order = deal_dao.getDealOrderByHaID(haravan_id)

    if not deal_order.get('data',None):
        print('HaravanID chưa có trong database! Đang tạo mới Deal trên Bitrix24')
        return create_deal_bitrix(payload)

    fields = Deal.HaravanToBitrix24(payload)
    fields['STAGE_ID'] = "C18:WON"
    # Tạo deal mới trên bitrix
    result = bitrix24_service.Deal.update(fields)
    if not result:
        print('Cập nhật Deal trên Bitrix24 thất bại!')
        return False
    return deal_dao.updateDeal(haravan_id, json.dumps(payload), json.dumps(result))


def delete_deal_bitrix(id):
    today = datetime.now()
    # LOGGER.info("delete_deal_bitrix: ", extra={"today": today})
    deal_order = deal_dao.getDealOrderByHaID(id)

    if not deal_order.get('data',None) or deal_order['data'][0].get('status') == "DELETE":
        print('Bản ghi tbl_deal_order không tìm thấy!')
        return True
    # Xoá deal trên bitrix
    bitrix24_service.Deal.delete(deal_order['data'][0].get('bitrix24_id'))
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

    if payload.get("variants") :
        product["PRICE"] = payload.get("variants")[0].get("price")
        
        # DISCOUNT_TYPE_ID - where 1 - is the value in money; 2 - is the value in percentage
        product["DISCOUNT_TYPE_ID"] = 1 
        # DISCOUNT_RATE - the percentage of dicsount
        # product["DISCOUNT_RATE"] = 0 
        # DISCOUNT_RATE - the sum of discount
        product["DISCOUNT_SUM"] = payload.get("variants")[0].get("total_discount")
        
        if len(payload.get("images")) > 0:
            fileData = [payload.get("images")[0].get("src","https://vnztech.com/no-image.png")]
            product["PREVIEW_PICTURE"] = {'fileData':fileData}
            product["DETAIL_PICTURE"] = {'fileData':fileData}
    else:
        product["PRICE"] = 0

    bitrix24_data = bitrix24_service.Product.insert(fields=product)
    if bitrix24_data:
        product_dao.add_new_product(id, bitrix24_data.get("ID"), json.dumps(payload), json.dumps(bitrix24_data))
        return bitrix24_data

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
    if payload.get("phone"):
        contact["PHONE"] = [{
            "VALUE_TYPE": "WORK",
            "VALUE": payload.get("phone"),
            "TYPE_ID": "PHONE"
        }]
    if payload.get("email"):
        contact["EMAIL"] = [{
            "VALUE_TYPE": "WORK",
            "VALUE": payload.get("email"),
            "TYPE_ID": "EMAIL"
        }]

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


def migrate_customer_haravan_to_bitrix():
    # Lấy danh sách customer
    haravan_customers = haravan_service.Customer.list()
    # Su dung de test
    # haravan_customers = common.readJsonFile("data/haravan/blu-customers.json")
    print(haravan_customers)

    contacts = bitrix24_service.Contact.list()

    customers = haravan_customers.get("customers")

    # Migrate dữ liệu customer từ haravan sang cho bitrix
    for customer in customers:
        id = customer.get("id")
        haravan_contact = contact_dao.get_by_haravan_id(id)
        if haravan_contact:
            print('HaravanID đã có trong database! Tạo mới thất bại!')
            continue

        haravan_contact = find_contact_bitrix_by_email_phone(contacts, customer)

        # Đảm bảo dữ liệu từ haravan dc thêm vào bitrix 24
        # Nếu 2 hệ thống đã có dữ liệu mà chưa mapping vào hệ thống backend thì sẽ phải lưu lại và ko tạo lại sang bitrix nữa
        if haravan_contact:
            contact_dao.add_new_contact(id, haravan_contact.get("ID"), json.dumps(customer), json.dumps(haravan_contact))
            print('Cập nhật vào DB Contact thành công!')
            continue

        create_contact_bitrix(customer)

def migrate_product_haravan_to_bitrix():
    # Lấy danh sách customer
    haravan_products = haravan_service.Product.list()
    # haravan_products = common.readJsonFile("data/haravan/blu-customers.json")
    print(haravan_products)

    products = haravan_products.get("products")

    # Migrate dữ liệu customer từ haravan sang cho bitrix
    for product in products:
        id = product.get("id")
        haravan_contact = product_dao.get_by_haravan_id(id)
        if haravan_contact:
            print('HaravanID đã có trong database! Tạo mới thất bại!')
            continue

        product = mapping_service.convert_object(product, product_mapping, "BITRIX")

        bitrix24_data = bitrix24_service.Product.insert(fields=product)
        if bitrix24_data:
            product_dao.add_new_product(id, bitrix24_data.get("ID"), json.dumps(product), json.dumps(bitrix24_data))
            print('Tạo mới Product Bitrix24 thành công!')

def migrate_order_haravan_to_bitrix():
    # Lấy danh sách customer
    haravan_orders = haravan_service.Order.list()
    # haravan_products = common.readJsonFile("data/haravan/blu-customers.json")
    print(haravan_orders)

    orders = haravan_orders.get("orders")

    # Migrate dữ liệu customer từ haravan sang cho bitrix
    for order in orders:
        create_deal_bitrix(order)
    return haravan_orders

def find_contact_bitrix_by_email_phone(contacts, customer):
    if not contacts:
        return None
    phone = customer.get("phone")
    email = customer.get("email")
    for contact in contacts: #{"PHONE":[{"ID":"853377","VALUE_TYPE":"WORK","VALUE":"0915453110","TYPE_ID":"PHONE"}],"EMAIL":[{"ID":"853379","VALUE_TYPE":"WORK","VALUE":"haipb1982@gmail.com","TYPE_ID":"EMAIL"}]}
        contact_emails = contact.get("EMAIL")
        contact_phones = contact.get("PHONE")
        if contact_emails and len(contact_emails) > 0:
            for contact_email in contact_emails:
                if contact_email.get("VALUE") == email:
                    return contact
        if contact_phones and len(contact_phones) > 0:
            for contact_email in contact_phones:
                if contact_email.get("VALUE") == phone:
                    return contact
    return None

def testCon():
    print(deal_dao.getAllDeals())
    # print(contact_dao.getAllContacts())
    # print(product_dao.getAllProducts())

