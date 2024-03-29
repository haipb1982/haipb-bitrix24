import json

import dictdiffer

# from dao import deal_dao, product_dao, contact_dao

from mysqldb.dao.DealDAO import DealDAO
from mysqldb.dao.ProductDAO import ProductDAO 
from mysqldb.dao.ContactDAO import ContactDAO 

deal_dao = DealDAO()
product_dao = ProductDAO()
contact_dao = ContactDAO()

from services import bitrix24_service, mapping_service, haravan_service
from services.mapping_service import product_mapping, deal_mapping, contact_mapping
from utils import log

LOGGER = log.get_logger(__name__)


def create_order_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    deal_data = deal_dao.getBitrix24ID(id)

    if deal_data or (deal_data and (deal_data[0].get('status') == "DELETE")):
        return None

    deal_bitrix = bitrix24_service.Deal.get(id)

    if not deal_bitrix:
        return False

    # Nếu dữ liệu có thay đổi thì sẽ cho cập lại những thay đổi
    data = mapping_service.convert_object(deal_bitrix, deal_mapping, "HARAVAN")

    LOGGER.info("RESULT: ", extra={"extra": data})

    # TODO: Đây sẽ là dữ liệu tạm thời để có thể tạo order bitrix sang haravan
    # Cần lấy sản phẩm đúng thay vì mock sản phẩm
    product_variant_id = 1080334722

    haravan_data = {
        **data,
        "line_items": [
            {
                "variant_id": product_variant_id,
                "quantity": 1
            }
        ]}

    order_haravan = haravan_service.Order.create(haravan_data)

    # Xử lý nếu data haravan trả về đúng
    if order_haravan and order_haravan.get("order"):
        order = order_haravan.get("order")
        haravan_id = order.get("id")
        return deal_dao.addNewDeal(haravan_id, id, haravan_data=json.dumps(order), bitrix_data=json.dumps(deal_bitrix))
    else:
        return None

# Tạo record in tbl_deal_order
def delete_order_deal_if_existed(bitrix24_id):
    bx_data = bitrix24_service.Deal.get(bitrix24_id)
    if bx_data:
        haravan_id = bx_data.get('UF_CRM_1623809034975',None)
        if haravan_id:
            LOGGER.info(f'Tìm thấy HaravanID --> Thêm mới record tbl_deal_order... {haravan_id} {bitrix24_id}')
            result = deal_dao.addNewDeal(haravan_id, bitrix24_id, None, None)
            if result:
                LOGGER.info(f'Thêm mới record tbl_deal_order thành công! {haravan_id} {bitrix24_id}')
            else:
                LOGGER.info(f'Thêm mới record tbl_deal_order thất bại ! {haravan_id} {bitrix24_id}')
                LOGGER.info(f'Đang xoá Bx24 Deal {bitrix24_id} ...')
                _delete = bitrix24_service.Deal.delete(bitrix24_id) 
                LOGGER.info(f'--> Xoá Bx24 Deal {bitrix24_id}',extra={'extra':_delete})       
    else:
        LOGGER.info(f'Không có HaravanID trong Bx24 Deal {bitrix24_id}')
    return None

# Haravan chỉ cho phép chỉnh sửa note, shipping_address, tags còn những thong tin khác ko cho chỉnh sửa
# TODO: Sẽ cần xử lý về sau
def update_order_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    result = deal_dao.getBitrix24ID(id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu không có dữ liệu sẽ tạo mới record tbl_deal_order theo HaravanID trong Bx Deal
    if not result:
        delete_order_deal_if_existed(id) 
    
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if result[0].get('status') == "DELETE":
        return None

    haravan_id = result[0].get('haravan_id')

    old_data = json.loads(result[0].get('bitrix_data'))
    new_data = bitrix24_service.Deal.get(id)
    changed_data = get_changed_data(old_data, new_data)

    # Nếu data ko có gì sẽ thay đổi thì sẽ ko cần cập nhật vào haravan nữa tránh tình trạng bị trigger vòng tròn
    if not changed_data:
        return

    # Nếu dữ liệu có thay đổi thì sẽ cho cập lại những thay đổi
    data_update = mapping_service.convert_object(changed_data, deal_mapping, "HARAVAN")

    LOGGER.info("RESULT: ", extra={"extra": data_update})

    order_haravan = haravan_service.Order.update(haravan_id, data_update)

    if not order_haravan:
        return
    return deal_dao.updateDeal(haravan_id, haravan_data=json.dumps(order_haravan), bitrix_data=json.dumps(new_data))

def delete_order_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    result = deal_dao.getBitrix24ID(id)

    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if not result or result[0].get('status') == "DELETE":
        return None

    # Xóa dữ liệu được trigger từ bitrix trong DB -> Đánh dấu là DELETE
    deal_dao.delete_by_bitrix_id(id)

    haravan_id = result[0].get('haravan_id')

    status = haravan_service.Order.delete(haravan_id)

    if status:
        return deal_dao.delete_by_haravan_id(haravan_id)
    else:
        return None

def get_changed_data(old_data: dict, new_data: dict):
    differents = list(dictdiffer.diff(old_data, new_data))

    new = {}

    for diff in differents:
        if diff[0] == 'add' or diff[0] == 'change':
            new[diff[1]] = diff[2][1]
        elif diff[0] == 'remove':
            new[diff[1]] = ""

    return new


def create_product_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    product_data = product_dao.get_by_bitrix24_id(id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if product_data or (product_data and (product_data[5] == "DELETE" and product_data[6] == "DELETE")):
        return None

    product_bitrix = bitrix24_service.Product.get(id)

    data = mapping_service.convert_object(product_bitrix, product_mapping, "HARAVAN")

    # Cần phải mock data đẻ tạo được sản phẩm
    data = {
        "title": data.get("title"),
        "vendor": "Samsung",
        "product_type": "Khác",
    }

    product_haravan = haravan_service.Product.create(data)

    # Xử lý nếu data haravan trả về đúng
    if product_haravan and product_haravan.get("product"):
        product = product_haravan.get("product")
        haravan_id = product.get("id")
        return product_dao.add_new_product(haravan_id, id, haravan_data=json.dumps(product),
                                           bitrix_data=json.dumps(product_bitrix))
    else:
        return None


def update_product_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    product_data = product_dao.get_by_bitrix24_id(id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if not product_data or product_data[5] == "DELETE" and product_data[6] == "DELETE":
        return None

    haravan_id = product_data[1]

    old_data = json.loads(product_data[4])
    product_bitrix = bitrix24_service.Product.get(id)
    changed_data = get_changed_data(old_data, product_bitrix)

    # Nếu data ko có gì sẽ thay đổi thì sẽ ko cần cập nhật vào haravan nữa tránh tình trạng bị trigger vòng tròn
    if not changed_data:
        return

    data = mapping_service.convert_object(changed_data, product_mapping, "HARAVAN")

    # Cần phải mock data đẻ tạo được sản phẩm
    # data = {
    #     "title": data.get("title"),
    #     "vendor": "Samsung",
    #     "product_type": "Khác",
    # }

    product_haravan = haravan_service.Product.update(haravan_id, data)

    # Xử lý nếu data haravan trả về đúng
    if product_haravan and product_haravan.get("product"):
        product = product_haravan.get("product")
        return product_dao.update_by_haravan_id(haravan_id, haravan_data=json.dumps(product),
                                                bitrix_data=json.dumps(product_bitrix))
    else:
        return None


def delete_product_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    product_data = product_dao.get_by_bitrix24_id(id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if not product_data or product_data[5] == "DELETE" and product_data[6] == "DELETE":
        return None

    # Xóa dữ liệu được trigger từ bitrix trong DB -> Đánh dấu là DELETE
    product_dao.delete_by_bitrix_id(id)

    # Sau khi cập nhật bitrix trong DB sẽ xóa product haravan và cập nhật lại vào DB
    haravan_id = product_data[1]
    status = haravan_service.Product.delete(haravan_id)

    if status:
        return product_dao.delete_by_haravan_id(haravan_id)
    else:
        return None

def create_contact_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    contact_data = contact_dao.get_by_bitrix24_id(id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if contact_data or (contact_data and (contact_data[5] == "DELETE" and contact_data[6] == "DELETE")):
        return None

    contact_bitrix = bitrix24_service.Contact.get(id)

    data = mapping_service.convert_object(contact_bitrix, contact_mapping, "HARAVAN")

    # Cần phải mock data đẻ tạo được sản phẩm
    contact_haravan = haravan_service.Customer.create(data)

    # Xử lý nếu data haravan trả về đúng
    if contact_haravan and contact_haravan.get("customer"):
        customer = contact_haravan.get("customer")
        haravan_id = customer.get("id")
        return contact_dao.add_new_contact(haravan_id, id, haravan_data=json.dumps(customer),
                                           bitrix_data=json.dumps(contact_bitrix))
    else:
        return None

def update_contact_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    contact_data = contact_dao.get_by_bitrix24_id(id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if not contact_data or contact_data[5] == "DELETE" and contact_data[6] == "DELETE":
        return None

    haravan_id = contact_data[1]

    old_data = json.loads(contact_data[4])
    contact_bitrix = bitrix24_service.Contact.get(id)
    changed_data = get_changed_data(old_data, contact_bitrix)

    # Nếu data ko có gì sẽ thay đổi thì sẽ ko cần cập nhật vào haravan nữa tránh tình trạng bị trigger vòng tròn
    if not changed_data:
        return

    data = mapping_service.convert_object(changed_data, contact_mapping, "HARAVAN")

    contact_haravan = haravan_service.Customer.update(haravan_id, data)

    # Xử lý nếu data haravan trả về đúng
    if contact_haravan and contact_haravan.get("product"):
        contact = contact_haravan.get("product")
        return contact_dao.update_by_haravan_id(haravan_id, haravan_data=json.dumps(contact),
                                                bitrix_data=json.dumps(contact_haravan))
    else:
        return None

def delete_contact_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    contact_data = contact_dao.get_by_bitrix24_id(id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if not contact_data or contact_data[5] == "DELETE" and contact_data[6] == "DELETE":
        return None

    # Xóa dữ liệu được trigger từ bitrix trong DB -> Đánh dấu là DELETE
    contact_dao.delete_by_bitrix_id(id)

    # Sau khi cập nhật bitrix trong DB sẽ xóa product haravan và cập nhật lại vào DB
    haravan_id = contact_data[1]
    status = haravan_service.Customer.delete(haravan_id)

    if status:
        return contact_dao.delete_by_haravan_id(haravan_id)
    else:
        return None
