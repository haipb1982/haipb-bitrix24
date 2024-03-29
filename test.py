from services import haravan_to_bitrix, bitrix_to_haravan

from mysqldb.dao.DealDAO import DealDAO 

from mysqldb.dao.ProductDAO import ProductDAO 

body = {
        "billing_address": {
            "address1": "11 bis nguy\u1ec5n gia thi\u1ec1u,",
            "address2": None,
            "city": None,
            "company": None,
            "country": "Vietnam",
            "first_name": "10/10",
            "id": 1054395139,
            "last_name": "Anh Khoa",
            "phone": "0793501097",
            "province": "H\u1ed3 Ch\u00ed Minh",
            "zip": None,
            "name": "Anh Khoa 10/10",
            "province_code": "HC",
            "country_code": "VN",
            "default": True,
            "district": "Qu\u1eadn 3",
            "district_code": "HC468",
            "ward": None,
            "ward_code": None
        },
        "browser_ip": None,
        "buyer_accepts_marketing": False,
        "cancel_reason": None,
        "cancelled_at": None,
        "cart_token": "ec384b9b5f7e4098b2e57def23f30a74",
        "checkout_token": "ec384b9b5f7e4098b2e57def23f30a74",
        "client_details": {
            "accept_language": None,
            "browser_ip": None,
            "session_hash": None,
            "user_agent": None,
            "browser_height": None,
            "browser_width": None
        },
        "closed_at": None,
        "created_at": "2021-11-13T13:43:40.745Z",
        "currency": "VND",
        "customer": {
            "accepts_marketing": False,
            "addresses": [
                {
                    "address1": "11 bis nguy\u1ec5n gia thi\u1ec1u,",
                    "address2": None,
                    "city": None,
                    "company": None,
                    "country": "Vietnam",
                    "first_name": "10/10",
                    "id": 1089507191,
                    "last_name": "Anh Khoa",
                    "phone": "0793501097",
                    "province": "H\u1ed3 Ch\u00ed Minh",
                    "zip": None,
                    "name": "Anh Khoa 10/10",
                    "province_code": "HC",
                    "country_code": "VN",
                    "default": False,
                    "district": "Qu\u1eadn 3",
                    "district_code": "HC468",
                    "ward": None,
                    "ward_code": None
                },
                {
                    "address1": "11 bis nguy\u1ec5n gia thi\u1ec1u,",
                    "address2": None,
                    "city": None,
                    "company": None,
                    "country": "Vietnam",
                    "first_name": "Anh Khoa 10/10",
                    "id": 1089507019,
                    "last_name": None,
                    "phone": "0793501097",
                    "province": "H\u1ed3 Ch\u00ed Minh",
                    "zip": None,
                    "name": "Anh Khoa 10/10",
                    "province_code": "HC",
                    "country_code": "VN",
                    "default": True,
                    "district": "Qu\u1eadn 3",
                    "district_code": "HC468",
                    "ward": None,
                    "ward_code": None
                }
            ],
            "created_at": "2021-11-13T13:40:30.142Z",
            "default_address": None,
            "email": "khoatran93yds@gmail.com",
            "phone": "0793501097",
            "first_name": "Anh Khoa 10/10",
            "id": 1054395139,
            "last_name": None,
            "last_order_id": 1242402884,
            "last_order_name": "WEB102998",
            "note": None,
            "orders_count": 1,
            "state": "disabled",
            "tags": None,
            "total_spent": 4557150,
            "updated_at": "2021-11-13T13:43:41Z",
            "verified_email": False,
            "birthday": None,
            "gender": 1,
            "last_order_date": "2021-11-13T13:43:41Z",
            "multipass_identifier": None
        },
        "discount_codes": [
            {
                "amount": 239850,
                "code": "\u01afU \u0110\u00c3I 20/11",
                "type": "percentage",
                "is_coupon_code": False
            }
        ],
        "email": "khoatran93yds@gmail.com",
        "financial_status": "paid",
        "fulfillments": [],
        "fulfillment_status": "notfulfilled",
        "tags": "",
        "gateway": "Chuy\u1ec3n kho\u1ea3n - Banking Transfer",
        "gateway_code": "bankdeposit",
        "id": 1242402884,
        "landing_site": None,
        "landing_site_ref": None,
        "source": "haravan_draft_order",
        "line_items": [
            {
                "fulfillable_quantity": 1,
                "fulfillment_service": None,
                "fulfillment_status": "notfulfilled",
                "grams": 100,
                "id": 1334433323,
                "price": 1499000,
                "price_original": 1499000,
                "price_promotion": 0,
                "product_id": 1018226873,
                "quantity": 1,
                "requires_shipping": True,
                "sku": "BLHBB0031A",
                "title": "Hermes - Ng\u1ecdc Trai \u0110en Tahiti - M\u1ea1 Gold Titanium",
                "variant_id": 1036083436,
                "variant_title": "M\u1ea1 Gold Titanium / M(0.7 mm) / Xanh",
                "vendor": "BLUSAIGON",
                "type": "B\u00fat Ng\u1ecdc Trai",
                "name": "Hermes - Ng\u1ecdc Trai \u0110en Tahiti - M\u1ea1 Gold Titanium - M\u1ea1 Gold Titanium / M(0.7 mm) / Xanh",
                "gift_card": False,
                "taxable": True,
                "tax_lines": None,
                "product_exists": True,
                "barcode": "8938513309070",
                "properties": [],
                "applied_discounts": [],
                "total_discount": 0,
                "image": {
                    "src": "https://product.hstatic.net/1000345452/product/21_0b3c2881ce3348d4b9b1a648317a63c3.png"
                },
                "not_allow_promotion": False,
                "ma_cost_amount": 600000
            },
            {
                "fulfillable_quantity": 1,
                "fulfillment_service": None,
                "fulfillment_status": "notfulfilled",
                "grams": 100,
                "id": 1334433324,
                "price": 1499000,
                "price_original": 1499000,
                "price_promotion": 0,
                "product_id": 1018226871,
                "quantity": 1,
                "requires_shipping": True,
                "sku": "BLHWW0031A",
                "title": "Hermes - Ng\u1ecdc Trai Tr\u1eafng B\u1eafc \u00dac - M\u1ea1 Gold Titanium",
                "variant_id": 1036083434,
                "variant_title": "M\u1ea1 Gold Titanium / M(0.7 mm) / Xanh",
                "vendor": "BLUSAIGON",
                "type": "B\u00fat Ng\u1ecdc Trai",
                "name": "Hermes - Ng\u1ecdc Trai Tr\u1eafng B\u1eafc \u00dac - M\u1ea1 Gold Titanium - M\u1ea1 Gold Titanium / M(0.7 mm) / Xanh",
                "gift_card": False,
                "taxable": True,
                "tax_lines": None,
                "product_exists": True,
                "barcode": "8938513309063",
                "properties": [],
                "applied_discounts": [],
                "total_discount": 0,
                "image": {
                    "src": "https://product.hstatic.net/1000345452/product/1_199dfbcfcd6c4c948136a634ebd2f899.png"
                },
                "not_allow_promotion": False,
                "ma_cost_amount": 600000
            },
            {
                "fulfillable_quantity": 1,
                "fulfillment_service": None,
                "fulfillment_status": "notfulfilled",
                "grams": 0,
                "id": 1334433325,
                "price": 1799000,
                "price_original": 1799000,
                "price_promotion": 0,
                "product_id": 1028611807,
                "quantity": 1,
                "requires_shipping": False,
                "sku": "BLHPP0031A",
                "title": "Hermes - B\u00fat Bi Ng\u1ecdc Trai H\u1ed3ng Mississipi - M\u1ea1 Gold Titanium",
                "variant_id": 1062769914,
                "variant_title": "M\u1ea1 Gold Titanium / M(0.7 mm) / Xanh",
                "vendor": "BLUSAIGON",
                "type": "B\u00fat Ng\u1ecdc Trai",
                "name": "Hermes - B\u00fat Bi Ng\u1ecdc Trai H\u1ed3ng Mississipi - M\u1ea1 Gold Titanium - M\u1ea1 Gold Titanium / M(0.7 mm) / Xanh",
                "gift_card": False,
                "taxable": True,
                "tax_lines": None,
                "product_exists": True,
                "barcode": "8938513309469",
                "properties": [],
                "applied_discounts": [],
                "total_discount": 0,
                "image": {
                    "src": "https://product.hstatic.net/1000345452/product/27_799ab2e4a53a46e28aca3e92cb41df47.png"
                },
                "not_allow_promotion": False,
                "ma_cost_amount": 600000
            },
            {
                "fulfillable_quantity": 3,
                "fulfillment_service": None,
                "fulfillment_status": "notfulfilled",
                "grams": 0,
                "id": 1334433326,
                "price": 0,
                "price_original": 500000,
                "price_promotion": 0,
                "product_id": 1029302712,
                "quantity": 3,
                "requires_shipping": True,
                "sku": "BLBX002",
                "title": "BO04 - H\u1ed9p Xanh Gi\u1ea5y Cao C\u1ea5p - B\u00fat & Khuy M\u0103ng S\u00e9t",
                "variant_id": 1065063751,
                "variant_title": "Xanh",
                "vendor": "BLUSaigon",
                "type": "H\u1ed9p B\u00fat",
                "name": "BO04 - H\u1ed9p Xanh Gi\u1ea5y Cao C\u1ea5p - B\u00fat & Khuy M\u0103ng S\u00e9t - Xanh",
                "gift_card": False,
                "taxable": True,
                "tax_lines": None,
                "product_exists": True,
                "barcode": None,
                "properties": [],
                "applied_discounts": [
                    {
                        "description": None,
                        "amount": 500000
                    }
                ],
                "total_discount": 500000,
                "image": {
                    "src": "https://product.hstatic.net/1000345452/product/qt014017_12cdb2bacc1949aa95d66e4b43725d87_large_7e6b9a38d61f4cfc80638a65459e782a.png"
                },
                "not_allow_promotion": False,
                "ma_cost_amount": 100732.76
            }
        ],
        "name": "WEB102998",
        "note": "Th\u1eddi gian giao h\u00e0ng : \u0110\u1ea7u tu\u1ea7n sau.\n",
        "number": 1242402884,
        "order_number": "WEB102998",
        "processing_method": None,
        "referring_site": "haravan_draft_order",
        "refunds": [],
        "shipping_address": {
            "address1": "11 bis Nguy\u1ec5n Gia Thi\u1ec1u,",
            "address2": None,
            "city": None,
            "company": None,
            "country": "Vietnam",
            "first_name": "10/10",
            "last_name": "Anh Khoa",
            "latitude": None,
            "longitude": None,
            "phone": "0793501097",
            "province": "H\u1ed3 Ch\u00ed Minh",
            "zip": None,
            "name": "Anh Khoa 10/10",
            "province_code": "HC",
            "country_code": "VN",
            "district_code": "HC468",
            "district": "Qu\u1eadn 3",
            "ward_code": None,
            "ward": None
        },
        "shipping_lines": [
            {
                "code": None,
                "price": 0,
                "source": None,
                "title": None
            }
        ],
        "source_name": "haravan_draft_order",
        "subtotal_price": 4797000,
        "tax_lines": None,
        "taxes_included": False,
        "token": "ec384b9b5f7e4098b2e57def23f30a74",
        "total_discounts": 239850,
        "total_line_items_price": 4797000,
        "total_price": 4557150,
        "total_tax": 0,
        "total_weight": 200,
        "updated_at": "2021-11-14T02:57:58.389Z",
        "transactions": [
            {
                "amount": 4557150,
                "authorization": None,
                "created_at": "2021-11-13T13:43:40.984Z",
                "device_id": None,
                "gateway": "Chuy\u1ec3n kho\u1ea3n - Banking Transfer",
                "id": 1098834577,
                "kind": "pending",
                "order_id": 1242402884,
                "receipt": None,
                "status": None,
                "user_id": 200000571759,
                "location_id": 580756,
                "payment_details": None,
                "parent_id": None,
                "currency": None,
                "haravan_transaction_id": None,
                "external_transaction_id": None
            },
            {
                "amount": 4557150,
                "authorization": None,
                "created_at": "2021-11-13T13:43:41.015Z",
                "device_id": None,
                "gateway": "Chuy\u1ec3n kho\u1ea3n - Banking Transfer",
                "id": 1098834578,
                "kind": "capture",
                "order_id": 1242402884,
                "receipt": None,
                "status": None,
                "user_id": 200000571759,
                "location_id": 580756,
                "payment_details": None,
                "parent_id": None,
                "currency": None,
                "haravan_transaction_id": None,
                "external_transaction_id": None
            }
        ],
        "note_attributes": [],
        "confirmed_at": "2021-11-13T13:43:41.244Z",
        "closed_status": "unclosed",
        "cancelled_status": "uncancelled",
        "confirmed_status": "confirmed",
        "assigned_location_id": None,
        "assigned_location_at": None,
        "exported_confirm_at": None,
        "user_id": 200000571759,
        "device_id": None,
        "location_id": 580756,
        "ref_order_id": 0,
        "ref_order_number": None,
        "utm_source": None,
        "utm_medium": None,
        "utm_campaign": None,
        "utm_term": None,
        "utm_content": None,
        "payment_url": None,
        "contact_email": "khoatran93yds@gmail.com",
        "order_processing_status": "confirmed",
        "redeem_model": None
    }

# haravan_to_bitrix.update_deal_bitrix(body)

# print(DealDAO())
_dealDAO = DealDAO()
# _dealDAO.getHaravanID(1242402884)

# addNewDeal 1242398867 204
resutl = _dealDAO.addNewDeal(1, 1,'-','-')
print(resutl)

# _productDAO = ProductDAO()

# r = _productDAO.add_new_product(1,1,'','')
# print(r)

