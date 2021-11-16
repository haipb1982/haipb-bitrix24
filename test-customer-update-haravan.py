from services import haravan_to_bitrix, bitrix_to_haravan

from mysqldb.dao.DealDAO import DealDAO 

from mysqldb.dao.ProductDAO import ProductDAO 

haravan_id = 1054492585

body_update = {"accepts_marketing": False, "addresses": [{"address1": "608 N2D Trung Hoa Nhan Chinh Thanh Xuan", "address2": None, "city": None, "company": None, "country": "Vietnam", "first_name": "Hai", "id": 1089639275, "last_name": "Phan Ba", "phone": "0915453110", "province": "H\u00e0 N\u1ed9i", "zip": None, "name": "Phan Ba Hai", "province_code": "HI", "country_code": "VN", "default": True, "district": "Qu\u1eadn Thanh Xu\u00e2n", "district_code": "HI7", "ward": "Ph\u01b0\u1eddng Nh\u00e2n Ch\u00ednh", "ward_code": "00343"}], "created_at": "2021-11-15T22:52:58.637Z", "default_address": {"address1": "608 N2D Trung Hoa Nhan Chinh Thanh Xuan", "address2": None, "city": None, "company": None, "country": "Vietnam", "first_name": "Hai", "id": 1089639275, "last_name": "Phan Ba", "phone": "0915453110", "province": "H\u00e0 N\u1ed9i", "zip": None, "name": "Phan Ba Hai", "province_code": "HI", "country_code": "VN", "default": True, "district": "Qu\u1eadn Thanh Xu\u00e2n", "district_code": "HI7", "ward": "Ph\u01b0\u1eddng Nh\u00e2n Ch\u00ednh", "ward_code": "00343"}, "email": "haipb@gmail.com", "phone": "0989898989", "first_name": "Hai 000", "id": haravan_id, "last_name": "Phan Ba 123", "last_order_id": None, "last_order_name": None, "note": "tech lead in vlance", "orders_count": 0, "state": "disabled", "tags": None, "total_spent": 0, "updated_at": "2021-11-15T22:53:04.845Z", "verified_email": False, "birthday": "1982-07-04T00:00:00Z", "gender": 1, "last_order_date": None, "multipass_identifier": None}

# haravan_to_bitrix.create_contact_bitrix(body_update)

# haravan_to_bitrix.update_deal_bitrix(body_update)
