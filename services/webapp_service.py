from .mapping_service import convert_object, product_mapping, contact_mapping
import migration.deal as Deal
from utils import log, common
import json
from calendar import mdays
from datetime import datetime, timedelta

from . import bitrix24_service as bx24, bitrix24_service, mapping_service, haravan_service
# from dao import deal_dao, product_dao, contact_dao
from mysqldb.dao.DealDAO import DealDAO
from mysqldb.dao.ProductDAO import ProductDAO
from mysqldb.dao.ContactDAO import ContactDAO
from .bitrix24_service import DealProductRow
from services import haravan_service

deal_dao = DealDAO()
product_dao = ProductDAO()
contact_dao = ContactDAO()


LOGGER = log.get_logger(__name__)


def get_all_orders():
    return deal_dao.getAllDeals()


def get_all_orders_pages(from_page, to_page):
    return deal_dao.getAllDealsPages(from_page, to_page)


def delete_order_record(id):
    return deal_dao.deleteDealRecord(id)


def update_order_record(id, haravan_id, bitrix24_id):
    return deal_dao.updateDealRecord(id, haravan_id, bitrix24_id)


def insert_order_record(haravan_id, bitrix24_id):
    return deal_dao.insertDealRecord(haravan_id, bitrix24_id)

#######################################


def get_all_products():
    return product_dao.getAllProducts()


def get_all_products_pages(from_page, to_page):
    return product_dao.getAllProductsPages(from_page, to_page)


def delete_product_record(id):
    return product_dao.deleteProductRecord(id)


def update_product_record(id, haravan_id, bitrix24_id):
    return product_dao.updateProductRecord(id, haravan_id, bitrix24_id)


def insert_product_record(haravan_id, bitrix24_id):
    return product_dao.insertProductRecord(haravan_id, bitrix24_id)

#######################################


def get_all_contacts():
    return contact_dao.getAllContacts()


def get_all_contacts_pages(from_page, to_page):
    return contact_dao.getAllContactsPages(from_page, to_page)


def delete_contact_record(id):
    return contact_dao.deleteContactRecord(id)


def update_contact_record(id, haravan_id, bitrix24_id):
    return contact_dao.updateContactRecord(id, haravan_id, bitrix24_id)


def insert_contact_record(haravan_id, bitrix24_id):
    return contact_dao.insertContactRecord(haravan_id, bitrix24_id)


# Sync data bằng cách cập nhật update_ts order, product, contact. Sau đó auto trigger webhook để đồng bộ 2 chiều
def get_sync(type, haravan_id):
    LOGGER.info(f'Sync data {type} from Haravan ID={haravan_id}')
    res = {}
    res['code'] = 200
    res['message'] = 'SYNC data successful!'
    res['data'] = None
    data = {'tags': 'sync at '+ datetime.now().replace(microsecond=0).isoformat()}
    try:
        if type in ['order','orders'] :
            deal_dao.updateDeal(id=haravan_id)
            res['data'] = haravan_service.Order.update(haravan_id, data)
        elif type in ['product','products']:
            res['data'] = haravan_service.Product.update(haravan_id, data)
        elif type in ['contact','contacts']:
            res['data'] = haravan_service.Customer.update(haravan_id, data)
        else:
            res['message'] = 'NOT found type! SYNC data failed...'
        
    except:
        res['code'] = 500
        res['message'] = 'SYNC data failed!'

    return res

def check_duplicates():
    
    latest_id = deal_dao.getMaxDealID().get('data',None)
    if not latest_id:
        return

    latest_id = latest_id[0].get('bitrix24_id')
    check_numbers = 10
    while latest_id < latest_id + check_numbers:
        # print(id)
        try:
            data = bitrix24_service.Deal.get(latest_id)
            if data:
                ha_id = data.get('UF_CRM_1623809034975', None)
                if ha_id:
                    # Nếu có ha_id tìm record tbl_deal_order
                    dao = deal_dao.getDealOrderByHaID(ha_id)
                    # print(dao)

                    if dao.get('data',None):
                        bx_id = dao['data'][0].get('bitrix24_id', None)

                        if bx_id:
                            # Nếu có bx_id so sánh với id
                            if not latest_id == bx_id:
                                # Nếu id khác bx_id xoá Deal=id
                                bitrix24_service.Deal.delete(latest_id)
                    else:
                        # Nếu không có ha_id thêm mới record tbl_deal_order
                        print(deal_dao.addNewDeal(ha_id, latest_id, None, None))
        except Exception as err:
            # retry_dao.insertRetryJobRecord(bitrix24_id=latest_id)
            print(f'ERROR {latest_id}: ', err)

    latest_id += 2
