import json
import requests
from bitrix24 import *
from datetime import datetime
import migration.deal as Deal


# bx24 = Bitrix24('https://blusaigon.bitrix24.com/rest/2069/pc3dgsz0s0ohfz6v/crm.deal.fields.json')
bx24 = Bitrix24('https://b24-hfk65b.bitrix24.com/rest/1/ppyzdjwvsgune1od/crm.deal.fields.json') # TuanNA

# # # # # # 

# # # # # # # # # # # # # # # DEAL FUNCTIONS # # # # # # # # # # # # # # # 
deal = {
         'TITLE': 'HAIPB TEST DEAL 28-10-2021-111', 'TYPE_ID': '', 'STAGE_ID': "C18:NEW", 'PROBABILITY': '', 'CURRENCY_ID': 'VND', 'OPPORTUNITY': 686868, 'IS_MANUAL_OPPORTUNITY': 'N', 'TAX_VALUE': '', 'LEAD_ID': '', 'COMPANY_ID': '0', 'CONTACT_ID': 236901, 'QUOTE_ID': '', 'BEGINDATE': datetime.now(), 'CLOSEDATE': datetime.now(), 'ASSIGNED_BY_ID': 1, 'CREATED_BY_ID': 7, 'MODIFY_BY_ID': 7, 'DATE_CREATE': datetime.now(), 'DATE_MODIFY': datetime.now(), 'OPENED': 'N', 'CLOSED': 'N', 'COMMENTS': '', 'ADDITIONAL_INFO': '', 'LOCATION_ID': '', 'CATEGORY_ID': 18, 'STAGE_SEMANTIC_ID': 'P', 'IS_NEW': 'Y', 'IS_RECURRING': 'N', 'IS_RETURN_CUSTOMER': 'N', 'IS_REPEATED_APPROACH': 'N', 'SOURCE_ID': '', 'SOURCE_DESCRIPTION': '', 'ORIGINATOR_ID': 33, 'ORIGIN_ID': 34, 'UTM_SOURCE': 35, 'UTM_MEDIUM': 36, 'UTM_CAMPAIGN': 37, 'UTM_CONTENT': 38, 'UTM_TERM': 39, 'UF_CRM_1626419521': 40, 'UF_CRM_1626419645': 41, 'UF_CRM_1626419711': 42, 'UF_CRM_1626419773': 43, 'UF_CRM_60FE433E3FBFC': 44, 'UF_CRM_60FE433E5FD29': 45, 'UF_CRM_1629079188': 46, 'UF_CRM_1627457986': 47, 'UF_CRM_1627606315': 48, 'UF_CRM_1627873425': 49, 'UF_CRM_1627873492': 50, 'UF_CRM_1627875523': 51, 'UF_CRM_1627875873': 52, 'UF_CRM_1628132442': 53, 'UF_CRM_1628132482': 54, 'UF_CRM_1628131833': 55, 'UF_CRM_1628155141': 56, 'UF_CRM_HANA_LEAD_ID': 57, 'UF_CRM_HANA_DEAL_ID': 58, 'UF_CRM_HANA_CHAT_URL': 59, 'UF_CRM_5F7C716902967': 60, 'UF_CRM_1623725469652': 61, 'UF_CRM_1623809034975': 62, 'UF_CRM_1628149922667': 63, 'UF_CRM_1628149948721': 64, 'UF_CRM_1628149984252': 65, 'UF_CRM_1629336877': 66, 'UF_CRM_61208953B806D': 67, 'UF_CRM_1630139611544': 68, 'UF_CRM_1630143314980': 69, 'UF_CRM_1630143954760': 70, 'UF_CRM_1630416306053': 71, 'UF_CRM_1630417157521': 72, 'UF_CRM_1630417292478': 73, 'UF_CRM_1630467922601': 74, 'UF_CRM_1630467958625': 75, 'UF_CRM_1630721600380': 76
        }
# deal = {
#     "TITLE": "Regular sale",
#     "TYPE_ID": "GOODS",
#     "STAGE_ID": "NEW",
#     "COMPANY_ID": 3,
#     "CONTACT_ID": 3,
#     "OPENED": "Y",
#     "ASSIGNED_BY_ID": 1,
#     "PROBABILITY": 30,
#     "CURRENCY_ID": "USD",
#     "OPPORTUNITY": 5000,
# }

def getDealList():
    res = bx24.callMethod('crm.deal.list')
    return res

def getDeal(dealID):
    res = bx24.callMethod("crm.deal.get", id=dealID)
    # print(res)
    return res

def getField():
    res = bx24.callMethod("crm.deal.fields")
    # print(res)

    return res

def addNewDeal(fields):
    try:
        id = bx24.callMethod("crm.deal.add", fields = fields,
                             params = { "REGISTER_SONET_EVENT": "Y" }	)

        return id

    except BitrixError as message:
        print(message)
        return None


def updateDeal(data_fields):
    # xu ly haravan_request de pass data vao fields
    try:
        res = bx24.callMethod("crm.deal.update", id = data_fields.get("ID") , fields = data_fields)
        print(f'updateDeal: ', res)
        return True
    except Exception as e:
        print(e)
        return False

def deleteDeal(data_fields):
    try:
        res = bx24.callMethod("crm.deal.delete", id = data_fields.get("ID"))
        print(f'deleteDeal: ', res)
        return True
    except Exception as e:
        print(e)
        return False


# lay product by deal id
def getProductByDealID(dealID):
    res = bx24.callMethod("crm.deal.productrows.get", id=dealID)
    print(res)

# # # # # # # # # # # # # # # CONTACT FUNCTIONS # # # # # # # # # # # # # # # 

# lay contact by id
def getContactByID(contactID):
    print(contactID)
    res = bx24.callMethod("crm.contact.get", id = 236901 )
    return res

# lay contact id by phone
def getContactIDbyPhone():
    res = bx24.callMethod("crm.contact.list", filter = { "PHONE": "0915453110" })
    print(res)

# # # # # # # # # # # # # # # PRODUCT FUNCTIONS # # # # # # # # # # # # # # # 

# lay product list
def getProductListToFile():
    res = bx24.callMethod("crm.product.list")
    writeFile(res,"crm.contact.list.json")


# # # # # # # # # # # # # # # ULTIL FUNCTIONS # # # # # # # # # # # # # # # 

# ghi file
def writeFile(res,filename):
    f = open(filename, "w+",encoding='utf-8')
    f.write(json.dumps(res))
    f.close()

def readJsonFile(filename):
    # data = {}
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


# # # # # # 

# main
if __name__ == "__main__":
    print('rock!!!')
    # res = readJsonFile('blu-products.json')
    # for  item in res :
    #     sku = item['variants'][0]['sku']
    #     if not sku:
    #         print(item)
            # print(item['variants'][0]['sku'])
    # print(len(res))

    # print(addNewDeal())
    # print(getDeal(2))
    # res = bx24.callMethod("crm.deal.update", id = 3259 , fields = deal)
    # print(res)
    # fields = {
    #     "ID": "1",
    #     "TITLE": """ORDER\#1234""",
    #     "ADDITIONAL_INFO": "TEST",
    # }
    # id = bx24.callMethod("crm.deal.add", fields = fields,
    #                      params = { "REGISTER_SONET_EVENT": "Y" }	)
    # print(id)
    # res = bx24.callMethod("crm.deal.fields")
    # res = bx24.callMethod("crm.dealcategory.stage.list")
    # res = bx24.callMethod("crm.dealcategory.list")
    # print(json.dumps(res))
    #
    # res1 = bx24.callMethod("crm.deal.userfield.list")
    # res1 = bx24.callMethod("crm.deal.list")
    # res = bx24.callMethod("crm.product.property.list")
    # res = bx24.callMethod("crm.product.property.types")
    # res = bx24.callMethod("crm.productrow.list")
    # res = bx24.callMethod("crm.product.list")
    # res = bx24.callMethod("crm.product.property.list")
    # res = bx24.callMethod("crm.productsection.list")
    # print(json.dumps(res))
    # print(json.dumps(getDealList()))

    # payload = {"billing_address": {"address1": None, "address2": None, "city": None, "company": None, "country": "Vietnam", "first_name": None, "id": 1053472936, "last_name": None, "phone": None, "province": None, "zip": None, "name": "", "province_code": None, "country_code": "VN", "default": True, "district": None, "district_code": None, "ward": None, "ward_code": None}, "browser_ip": None, "buyer_accepts_marketing": False, "cancel_reason": None, "cancelled_at": None, "cart_token": "b3e448c11ed24d57b55cb60770ee3491", "checkout_token": "b3e448c11ed24d57b55cb60770ee3491", "client_details": {"accept_language": None, "browser_ip": None, "session_hash": None, "user_agent": None, "browser_height": None, "browser_width": None}, "closed_at": None, "created_at": "2021-10-31T15:36:11.847Z", "currency": "VND", "customer": {"accepts_marketing": False, "addresses": [], "created_at": "2021-10-25T14:36:51.919Z", "default_address": None, "email": "guest@haravan.com", "phone": None, "first_name": None, "id": 1053472936, "last_name": None, "last_order_id": 1238522156, "last_order_name": "#100023", "note": "haipb", "orders_count": 7, "state": "disabled", "tags": None, "total_spent": 3320000, "updated_at": "2021-11-02T06:28:25Z", "verified_email": False, "birthday": None, "gender": None, "last_order_date": "2021-10-31T15:44:36Z", "multipass_identifier": None}, "discount_codes": [], "email": "guest@haravan.com", "financial_status": "paid", "fulfillments": [], "fulfillment_status": "notfulfilled", "tags": "", "gateway": "Chuy\u1ec3n kho\u1ea3n qua ng\u00e2n h\u00e0ng", "gateway_code": "bankdeposit", "id": 1238520665, "landing_site": None, "landing_site_ref": None, "source": "haravan_draft_order", "line_items": [{"fulfillable_quantity": 1, "fulfillment_service": None, "fulfillment_status": "notfulfilled", "grams": 0, "id": 1324848821, "price": 980000, "price_original": 980000, "price_promotion": 0, "product_id": 1035974156, "quantity": 1, "requires_shipping": True, "sku": None, "title": "\u0110\u1ed3ng h\u1ed3 th\u00f4ng minh smartwatch DZ09", "variant_id": 1079017264, "variant_title": "N\u00e2u", "vendor": "Apple", "type": "Kh\u00e1c", "name": "\u0110\u1ed3ng h\u1ed3 th\u00f4ng minh smartwatch DZ09 - N\u00e2u", "gift_card": False, "taxable": True, "tax_lines": None, "product_exists": True, "barcode": None, "properties": [], "applied_discounts": [], "total_discount": 0, "image": {"src": "https://product.hstatic.net/200000421849/product/44_6ce020f0-3215-48b2-ba8b-3aa5b099ab88_f6f12cdbf52d488282ddbf2b04d5bbfc.jpg"}, "not_allow_promotion": False, "ma_cost_amount": 0}], "name": "#100022", "note": "new orders", "number": 1238520665, "order_number": "#100022", "processing_method": None, "referring_site": "haravan_draft_order", "refunds": [], "shipping_address": {"address1": None, "address2": None, "city": None, "company": None, "country": "Vietnam", "first_name": None, "last_name": None, "latitude": None, "longitude": None, "phone": None, "province": None, "zip": None, "name": "", "province_code": None, "country_code": "VN", "district_code": None, "district": None, "ward_code": None, "ward": None}, "shipping_lines": [{"code": None, "price": 0, "source": None, "title": None}], "source_name": "haravan_draft_order", "subtotal_price": 980000, "tax_lines": None, "taxes_included": False, "token": "b3e448c11ed24d57b55cb60770ee3491", "total_discounts": 0, "total_line_items_price": 980000, "total_price": 980000, "total_tax": 0, "total_weight": 0, "updated_at": "2021-11-03T03:33:02.313Z", "transactions": [{"amount": 980000, "authorization": None, "created_at": "2021-10-31T15:36:11.885Z", "device_id": None, "gateway": "Chuy\u1ec3n kho\u1ea3n qua ng\u00e2n h\u00e0ng", "id": 1097043594, "kind": "pending", "order_id": 1238520665, "receipt": None, "status": None, "user_id": 200000905615, "location_id": 1181286, "payment_details": None, "parent_id": None, "currency": None, "haravan_transaction_id": None, "external_transaction_id": None}, {"amount": 980000, "authorization": None, "created_at": "2021-10-31T15:36:44.05Z", "device_id": None, "gateway": "Chuy\u1ec3n kho\u1ea3n qua ng\u00e2n h\u00e0ng", "id": 1097043631, "kind": "capture", "order_id": 1238520665, "receipt": None, "status": None, "user_id": 200000905615, "location_id": 1181286, "payment_details": None, "parent_id": 1097043594, "currency": None, "haravan_transaction_id": None, "external_transaction_id": None}], "note_attributes": [], "confirmed_at": "2021-10-31T15:36:12.036Z", "closed_status": "unclosed", "cancelled_status": "uncancelled", "confirmed_status": "confirmed", "assigned_location_id": None, "assigned_location_at": None, "exported_confirm_at": None, "user_id": 200000905615, "device_id": None, "location_id": 1181286, "ref_order_id": 0, "ref_order_number": None, "utm_source": None, "utm_medium": None, "utm_campaign": None, "utm_term": None, "utm_content": None, "payment_url": None, "contact_email": "guest@haravan.com", "order_processing_status": "confirmed", "redeem_model": None}
    # res = Deal.HaravanToBitrix24(payload)
    # print(res)
