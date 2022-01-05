from mysqldb.dao.DealDAO import DealDAO
from mysqldb.dao.ProductDAO import ProductDAO
from mysqldb.dao.ContactDAO import ContactDAO

deal_dao = DealDAO()
product_dao = ProductDAO()
contact_dao = ContactDAO()

deal_dao.insertDealRecord(111,222)