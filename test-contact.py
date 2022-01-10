from mysqldb.dao.DealDAO import DealDAO
from mysqldb.dao.ContactDAO import ContactDAO

from mysqldb.dao.RetryJobDAO import RetryJobDAO
from services import bitrix24_service, haravan_service, webapp_service, mapping_service

deal_dao = DealDAO()
contact_dao = ContactDAO()

# haravan_contact = contact_dao.get_by_haravan_id(1057215156)
# print(haravan_contact)

# print(mapping_service.get_changed_data(old,new))

new = {}
diff = ["change", ["addresses", 0, "first_name"], [None, "24/8/77"]]
diff =["change", ["addresses", 0, "id"], [1093340600, 1093342978]]
diff =["change", ["addresses", 0, "last_name"], ["Nguy\u1ec5n B\u1ea3o Ho\u00e0ng, 24/8/77", "Nguy\u1ec5n B\u1ea3o Ho\u00e0ng,"]]
diff =["add", "addresses", [[1, {"address1": None, "address2": None, "city": None, "company": None, "country": "Vietnam", "first_name": None, "id": 1093340600, "last_name": "Nguy\u1ec5n B\u1ea3o Ho\u00e0ng, 24/8/77", "phone": "0938620645", "province": None, "zip": None, "name": "Nguy\u1ec5n B\u1ea3o Ho\u00e0ng, 24/8/77", "province_code": None, "country_code": "VN", "default": true, "district": None, "district_code": None, "ward": None, "ward_code": None}]]]
if diff[0] == 'add' or diff[0] == 'change':
    new[diff[1]] = diff[2][1]
elif diff[0] == 'remove':
    new[diff[1]] = ""

print(new)