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

from utils import Logger, log, common
from utils.Logger import Logger
import migration.deal as Deal
from .mapping_service import convert_object, product_mapping, contact_mapping

# LOGGER = log.get_logger(__name__)
LOGGER = Logger(__name__).get()



def create_deal_bitrix(payload=None):
    LOGGER.info('Tạo mới Deal Bitrix24...')
    if payload is None:
        payload = {}
        return False

    # LOGGER.info("create_deal_bitrix: ", extra={"extra": payload})    

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id",None)
    deal_order = deal_dao.getDealOrderByHaID(haravan_id)

    if deal_order.get('data',None):
        LOGGER.info('HaravanID đã tồn tại trong database')
        return False

    # Lấy thông tin customer từ khách hàng để set cho CONTACT_ID. Nếu không có sẽ tạo mới customer
    customer = payload.get("customer")
    customer_id = customer.get("id",None)
    if customer_id:
        customer_contact_result = contact_dao.get_by_haravan_id(customer_id)

    if customer_contact_result:
        contact_bitrix_id = customer_contact_result.get("bitrix24_id")
        LOGGER.info('HaravanID đã tồn tại trong database')
    else:
        LOGGER.info('Tạo mới Contact Bx24...')
        contact_bitrix = create_contact_bitrix(customer)
        contact_bitrix_id = contact_bitrix.get("ID")
        LOGGER.info(f'Tạo mới Contact Bx24 thành công:{contact_bitrix_id}')


    fields = Deal.HaravanToBitrix24(payload)
    fields["CONTACT_ID"] = contact_bitrix_id

    # lấy thông tin người tạo từ haravan để gán cho bitrix
    user_id = payload.get("user_id")
    haravan_user = haravan_service.User.get(user_id)
    if haravan_user and haravan_user.get("user"):
        user = haravan_user.get("user")
        LOGGER.info('người tạo đơn',extra={'extra':user})
        fields['UF_CRM_1630417157521'] = user.get("last_name", "") + " " + user.get("first_name", "")
    else:
        fields['UF_CRM_1630417157521'] = 'HARAVAN-BITRIX24 APP' # người tạo đơn
        LOGGER.info('Không tìm thấy người tạo đơn mặc định --> HARAVAN-BITRIX24 APP')
    # fields["STAGE_ID"] = "C18:NEW"
    # fields["UF_CRM_1637252157269"] = str(payload.get("id"))

    # Tạo deal mới trên bitrix 
    
    bitrix24_deal = bitrix24_service.Deal.insert(fields)
    if not bitrix24_deal.get("ID"):
        LOGGER.error('Không tạo được Bitrix24 Deal mới!')
        return False
    else:
        LOGGER.info(f'Tạo mới Deal Bx24 thành công{bitrix24_deal.get("ID")}')
        
    LOGGER.info(f'Tạo mới record tbl_deal_order {haravan_id,bitrix24_deal.get("ID")}')
    add_new_result = deal_dao.addNewDeal(
        hanravan_id=haravan_id,
        bitrix24_id=bitrix24_deal.get("ID"),
        haravan_data=json.dumps(payload),
        bitrix_data=json.dumps(bitrix24_deal)
    )
    # Nếu không thành công thì chỉ add id và chạy update lại
    if not add_new_result:
        LOGGER.error(f'Tạo mới record tbl_deal_order lần 1 thất bại: {haravan_id} , {bitrix24_deal.get("ID")}')
    else:
        LOGGER.info(f'Tạo mới record tbl_deal_order lần 2 ... {haravan_id} , {bitrix24_deal.get("ID")}')
        add_new_result2 = deal_dao.addNewDeal(
        hanravan_id=haravan_id,
        bitrix24_id=bitrix24_deal.get("ID"),
        haravan_data=None,
        bitrix_data=None
        )
        if add_new_result2:
            update_deal_bitrix_all('orders/updated', payload)
        else:
            LOGGER.error(f'Tạo mới record tbl_deal_order lần 2 thất bại: {haravan_id} {bitrix24_deal.get("ID")}')
    
    update_deal_bitrix_all('orders/updated',payload)

    return True

def update_deal_bitrix_all(topic='', payload=None):
    if payload is None:
        payload = {}

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_id = payload.get("id") or payload.get("number")
    LOGGER.info(f'Cập nhật Haravan-->Bx24 update_deal_bitrix_all {haravan_id}')
    
    deal_order = deal_dao.getDealOrderByHaID(haravan_id)

    if not deal_order.get('data',None):
        LOGGER.warning('HaravanID chưa có trong database! Đang tạo mới Deal trên Bitrix24',extra={'extra':deal_order.get('data')})
        return create_deal_bitrix(payload)
    else:
        LOGGER.info('HaravanID có trong database!')

    # TODO: Với trường hợp update thì sẽ cần kiểm tra dữ liệu của webhook data so với dữ liệu trong DB.
    # Nếu khác nhau sẽ cho cập nhật

    LOGGER.info('So sánh dữ liệu tbl_deal_order')
    if Deal.CompareHaravanNewData(deal_order["data"][0], payload):
        LOGGER.info('No data changed! Không có thay đổi dữ liệu tbl_deal_order')
        return None
    else:
        LOGGER.info('Data changed in tbl_deal_order! continue updating...')


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
    
    LOGGER.info('Cập nhật dữ liệu trên bitrix',extra={'extra':fields})
    # Cập nhật deal trên bitrix
    result = bitrix24_service.Deal.update(fields)
    LOGGER.info('Cập nhật trên bitrix kết quả',extra={'extra':result})

    # Cập nhật products của Deal 
    product_haravans = payload.get("line_items",None)

    if not product_haravans:
        LOGGER.warning('Không có product trong Order Haravan')
        return None

    productrows = {}
    i = 0
    for product_haravan in product_haravans:
        if product_haravan.get("id",None):
            productrow = {}
            product_id  = None
            product_result = product_dao.get_by_haravan_id(product_haravan.get("id"))
            
            # Nếu có product trong tbl_product thì lấy bx24_id
            if product_result:
                LOGGER.info('Tìm thấy sản phẩm trong tbl_product')
                product_id = product_result.get("bitrix24_id")

            # Nếu không có product trong tbl_product thì tạo mới   
            else:
                LOGGER.info('Không Tìm thấy sản phẩm trong tbl_product. Tạo mới trên Bx24...')
                product = haravan_service.Product.get(product_haravan.get("id"))
                if product.get('product'):
                    product_bitrix = create_product_bitrix(product)
                    product_id = product_bitrix.get("ID")
                else:
                    LOGGER.warning(f'Không tìm thấy haravan product {product_haravan.get("id")}')

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
            if product_id:
                productrows[i] = productrow
                i = i + 1
        else:
            LOGGER.warning('Không tìm thấy product ID trong line_items')

    # Add products vào trong DEAL

    fields = {
        "id": fields["ID"],
        "rows": productrows
    }
    
    deal_productrow = DealProductRow.set(fields)
    LOGGER.info('Thêm mới DealProductRow vào Deal Bx24',extra={'extra':deal_productrow})

    LOGGER.info('Cập nhật dữ liệu trên tbl_deal_order')
    update_result = deal_dao.updateDeal(haravan_id, json.dumps(payload), json.dumps(result))
    if update_result:
        LOGGER.info('Cập nhật dữ liệu trên tbl_deal_order thành công')
    else:
        LOGGER.info('Cập nhật dữ liệu trên tbl_deal_order thất bại')
    return update_result

def delete_deal_bitrix(id):
    today = datetime.now()
    # LOGGER.info("delete_deal_bitrix: ", extra={"extra": today})
    deal_order = deal_dao.getDealOrderByHaID(id)

    if not deal_order.get('data',None) or deal_order['data'][0].get('status') == "DELETE":
        LOGGER.warning('Bản ghi tbl_deal_order không tìm thấy!')
        return True
    # Xoá deal trên bitrix
    bitrix24_service.Deal.delete(deal_order['data'][0].get('bitrix24_id'))
    return deal_dao.delete_by_haravan_id(id)

def create_product_bitrix(payload):
    
    id = payload.get("id",None)
    if not id:
        return None

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
    id = payload.get("id",None)
    if not id:
        return None

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
    id = payload.get("id",None)
    if not id:
        return None

    haravan_contact = contact_dao.get_by_haravan_id(id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if haravan_contact:
        LOGGER.info('HaravanID đã có trong database! Tạo mới thất bại!')
        return None
    if (haravan_contact and (haravan_contact.get("haravan_status") == "DELETE" and haravan_contact.get("bitrix_status") == "DELETE")):
        LOGGER.warning('HaravanID đã tồn tại trong database! Tạo mới thất bại!')
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
        LOGGER.info('Tạo mới Contact Bitrix24 thành công!')
        return bitrix24_data

    return None

def update_contact_bitrix(payload):
    haravan_id = payload.get("id",None)
    if not haravan_id:
        return None

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
    LOGGER.info(haravan_customers)

    contacts = bitrix24_service.Contact.list()

    customers = haravan_customers.get("customers")

    # Migrate dữ liệu customer từ haravan sang cho bitrix
    for customer in customers:
        id = customer.get("id")
        haravan_contact = contact_dao.get_by_haravan_id(id)
        if haravan_contact:
            LOGGER.info('HaravanID đã có trong database! Tạo mới thất bại!')
            continue

        haravan_contact = find_contact_bitrix_by_email_phone(contacts, customer)

        # Đảm bảo dữ liệu từ haravan dc thêm vào bitrix 24
        # Nếu 2 hệ thống đã có dữ liệu mà chưa mapping vào hệ thống backend thì sẽ phải lưu lại và ko tạo lại sang bitrix nữa
        if haravan_contact:
            contact_dao.add_new_contact(id, haravan_contact.get("ID"), json.dumps(customer), json.dumps(haravan_contact))
            LOGGER.info('Cập nhật vào DB Contact thành công!')
            continue

        create_contact_bitrix(customer)

def migrate_product_haravan_to_bitrix():
    # Lấy danh sách customer
    haravan_products = haravan_service.Product.list()
    # haravan_products = common.readJsonFile("data/haravan/blu-customers.json")
    LOGGER.info(haravan_products)

    products = haravan_products.get("products")

    # Migrate dữ liệu customer từ haravan sang cho bitrix
    for product in products:
        id = product.get("id")
        haravan_contact = product_dao.get_by_haravan_id(id)
        if haravan_contact:
            LOGGER.info('HaravanID đã có trong database! Tạo mới thất bại!')
            continue

        product = mapping_service.convert_object(product, product_mapping, "BITRIX")

        bitrix24_data = bitrix24_service.Product.insert(fields=product)
        if bitrix24_data:
            product_dao.add_new_product(id, bitrix24_data.get("ID"), json.dumps(product), json.dumps(bitrix24_data))
            LOGGER.info('Tạo mới Product Bitrix24 thành công!')

def migrate_order_haravan_to_bitrix():
    # Lấy danh sách customer
    haravan_orders = haravan_service.Order.list()
    # haravan_products = common.readJsonFile("data/haravan/blu-customers.json")
    LOGGER.info(haravan_orders)

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
    LOGGER.info(deal_dao.getAllDeals())
    # LOGGER.info(contact_dao.getAllContacts())
    # LOGGER.info(product_dao.getAllProducts())

