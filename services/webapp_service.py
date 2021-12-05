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

def get_all_orders():
    return deal_dao.getAllDeals()

def get_all_orders_pages(from_page, to_page):
    return deal_dao.getAllDealsPages(from_page, to_page)

def get_all_products():
    return product_dao.getAllProducts()

def get_all_products_pages(from_page, to_page):
    return product_dao.getAllProductsPages(from_page, to_page)

def get_all_contacts():
    return contact_dao.getAllContacts()

def get_all_contacts_pages(from_page, to_page):
    return contact_dao.getAllContactsPages(from_page, to_page)
    