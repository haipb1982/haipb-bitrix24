import json

import dictdiffer

from dao import deal_dao, product_dao
from services import bitrix24_service, mapping_service, haravan_service
from services.mapping_service import product_mapping, deal_mapping
from utils import log

LOGGER = log.get_logger(__name__)


def create_order_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    deal_data = deal_dao.getBitrix24ID(id)

    if deal_data or (deal_data and (deal_data[5] == "DELETE" and deal_data[6] == "DELETE")):
        return None

    deal_bitrix = bitrix24_service.Deal.get(id)

    if not deal_bitrix:
        return False

    # Nếu dữ liệu có thay đổi thì sẽ cho cập lại những thay đổi
    data = mapping_service.convert_object(deal_bitrix, deal_mapping, "HARAVAN")

    LOGGER.info("RESULT: ", extra={"data": data})

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

# Haravan chỉ cho phép chỉnh sửa note, shipping_address, tags còn những thong tin khác ko cho chỉnh sửa
# TODO: Sẽ cần xử lý về sau
def update_order_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    result = deal_dao.getBitrix24ID(id)

    # Nếu đã có dữ liệu để tạo thì sẽ không cần tạo lại nữa. Tránh trường hợp bitrix gửi sai hoặc bị vòng lặp
    # Nếu dữ liệu của haravan hoặc bitrix bị xóa thì sẽ ko cho xử lý
    if not result or result[5] == "DELETE" and result[6] == "DELETE":
        return None

    haravan_id = result[1]

    old_data = json.loads(result[4])
    new_data = bitrix24_service.Deal.get(id)
    changed_data = get_changed_data(old_data, new_data)

    # Nếu data ko có gì sẽ thay đổi thì sẽ ko cần cập nhật vào haravan nữa tránh tình trạng bị trigger vòng tròn
    if not changed_data:
        return

    # Nếu dữ liệu có thay đổi thì sẽ cho cập lại những thay đổi
    data_update = mapping_service.convert_object(changed_data, deal_mapping, "HARAVAN")

    LOGGER.info("RESULT: ", extra={"data_update": data_update})

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
    if not result or result[5] == "DELETE" and result[6] == "DELETE":
        return None

    # Xóa dữ liệu được trigger từ bitrix trong DB -> Đánh dấu là DELETE
    deal_dao.delete_by_bitrix_id(id)

    haravan_id = result[1]

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
    pass

def update_contact_haravan(id):
    pass

def delete_contact_haravan(id):
    pass