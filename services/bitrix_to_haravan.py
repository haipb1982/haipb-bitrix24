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

    if deal_data:
        return

    deal_bitrix = deal_dao.getBitrix24ID(id)

    if deal_bitrix:
        return False

    # Nếu dữ liệu có thay đổi thì sẽ cho cập lại những thay đổi
    data_update = mapping_service.convert_object(deal_bitrix, deal_mapping, "HARAVAN")

    LOGGER.info("RESULT: ", extra={"data_update": data_update})

    # new_deal = haravan_service.Order.create(haravan_id, data_update)
    #
    # if not new_deal:
    #     return
    # return deal_dao.updateDeal(haravan_id, haravan_data=json.dumps(new_deal),bitrix_data=json.dumps(new_data))


def update_order_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    result = deal_dao.getBitrix24ID(id)

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

    new_deal = haravan_service.Order.update(haravan_id, data_update)

    if not new_deal:
        return
    return deal_dao.updateDeal(haravan_id, haravan_data=json.dumps(new_deal), bitrix_data=json.dumps(new_data))


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
    if product_data:
        return None
    data = mapping_service.convert_object(product_data, product_mapping, "HARAVAN")

    product_haravan = haravan_service.Product.create(data)

    if product_haravan and product_haravan.get("product"):
        product = product_haravan.get("product")
        haravan_id = product.get("id")
        return product_dao.add_new_product(haravan_id, id, haravan_data=json.dumps(product),
                                           bitrix_data=json.dumps(product_data))
