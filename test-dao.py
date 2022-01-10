from mysqldb.dao.DealDAO import DealDAO
from mysqldb.dao.ProductDAO import ProductDAO
from mysqldb.dao.ContactDAO import ContactDAO
import time

deal_dao = DealDAO()
product_dao = ProductDAO()
contact_dao = ContactDAO()

# deal_dao.insertDealRecord(111,222)

 # test...
# while True:
#     t0 = time.time()
#     for i in range(10):
#         print(i)
#         print(deal_dao.getDealOrderByHaID(1259418605))
#     print("time cousumed:", time.time() - t0)


# ['WEB103364', 1259726417, '', '']
# deal_dao.updateNameRecord(name='WEB103364',haravan_id=1259726417)
res = deal_dao.getAllDeals()
print(len(res['data']))