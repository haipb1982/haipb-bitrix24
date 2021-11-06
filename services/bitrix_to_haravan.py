from dao import deal_dao
from services import bitrix24_service
from utils import log

LOGGER = log.get_logger(__name__)


def create_order_haravan(id):
    if not id:
        LOGGER.error("Can not get ID from event")
        return None

    result = deal_dao.getBitrix24ID(id)

    LOGGER.info("RESULT: ", extra={"result": result})

    bitrix_deal = bitrix24_service.Deal.get(id)

    if not bitrix_deal:
        return bitrix_deal


