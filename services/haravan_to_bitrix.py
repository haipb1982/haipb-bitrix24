from calendar import mdays
from datetime import datetime, timedelta

from flask import Flask

from . import bitrix24_service as bx24
from dao import deal_dao
from utils import log

LOGGER = log.get_logger(__name__)

app = Flask(__name__)


def create_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
    today = datetime.now()
    next_month_of_today = today + timedelta(mdays[today.month])
    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload, "today": today})
    id = payload.get("id")

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_order = deal_dao.getHaravanID(id)
    if haravan_order:
        return None, False
    fields = {
        "TITLE": "ORDER-" + payload.get("order_number").replace("#", ""),
        "ADDITIONAL_INFO": payload.get("note"),
        "OPPORTUNITY": payload.get("total_price"),
        "STAGE_ID": "NEW",
        # "CURRENCY_ID": "VND",
        "BEGINDATE": today,
        "CLOSEDATE": next_month_of_today
    }
    # Tạo deal mới trên bitrix
    bitrix24_id = bx24.add_new_deal(fields)
    # Lưu dữ liệu từ bitrix vào db để mapping giữa haravan và bitrix
    result = deal_dao.addNewDeal(hanravan_id=id, bitrix24_id=bitrix24_id, note="")
    return result, True


def update_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
    today = datetime.now()
    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload, "today": today})

    # Sử dụng database để mapping giữa haravan và bitrix
    id = payload.get("id")
    haravan_order = deal_dao.getHaravanID(id)
    if not haravan_order:
        return create_deal_bitrix(payload)
    fields = {
        "ID": haravan_order[2],
        "ADDITIONAL_INFO": payload.get("note"),
        "OPPORTUNITY": payload.get("total_price"),
    }
    # Tạo deal mới trên bitrix
    result = bx24.update_deal(fields)
    return result, True


def paid_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
    today = datetime.now()
    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload, "today": today})

    id = payload.get("id")
    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_order = deal_dao.getHaravanID(id)
    if not haravan_order:
        return create_deal_bitrix(payload)
    fields = {
        "ID": haravan_order[2],
        "STAGE_ID": "FINAL_INVOICE",
        # Trạng thái sẽ lấy từ dealcategory_stage.json -> Cần xác định trạng thái của hệ thống vì nó là dynamic
    }
    # Tạo deal mới trên bitrix
    result = bx24.update_deal(fields)
    return result, True


def cancelled_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
    today = datetime.now()
    LOGGER.info("create_deal_bitrix: ", extra={"payload": payload, "today": today})
    id = payload.get("id")

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_order = deal_dao.getHaravanID(id)
    if not haravan_order:
        return create_deal_bitrix(payload)
    fields = {
        "ID": haravan_order[2],
        "STAGE_ID": "LOSE",
    }
    # Tạo deal mới trên bitrix0
    result = bx24.update_deal(fields)
    return result, True


def fulfilled_deal_bitrix(payload=None):
    if payload is None:
        payload = {}
    today = datetime.now()
    LOGGER.info("fulfilled_deal_bitrix: ", extra={"payload": payload, "today": today})
    id = payload.get("id")

    # Sử dụng database để mapping giữa haravan và bitrix
    haravan_order = deal_dao.getHaravanID(id)
    if not haravan_order:
        return create_deal_bitrix(payload)
    fields = {
        "ID": haravan_order[2],
        "STAGE_ID": "WON",
    }
    # Tạo deal mới trên bitrix
    result = bx24.update_deal(fields)
    return result, True


def delete_deal_bitrix(id):
    today = datetime.now()
    LOGGER.info("delete_deal_bitrix: ", extra={"today": today})
    haravan_order = deal_dao.getHaravanID(id)
    if not haravan_order:
        return None, True
    # Tạo deal mới trên bitrix
    result = bx24.delete_deal(haravan_order[2])
    return result, True
