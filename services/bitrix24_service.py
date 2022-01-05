import json

from bitrix24 import *

from utils import log

LOGGER = log.get_logger(__name__)

bx24 = Bitrix24('https://blusaigon.bitrix24.com/rest/2069/nxf12nyf735bfbrl/')
# bx24 = Bitrix24('https://b24-0o3r9m.bitrix24.com/rest/1/om3gcd13tk2eca64/profile.json')  # TuanNA
# bx24 = Bitrix24('https://b24-nd8219.bitrix24.vn/rest/1/cjgdujez4jbs6nch/profile.json')  # HaiPB


class Deal():

    @staticmethod
    def list():
        try:
            res = bx24.callMethod('crm.deal.list')
            return res
        except BitrixError as e:
            LOGGER.error('BX24 list deal::exception: ', extra={"e": e})
            return None

    @staticmethod
    def get(dealID):
        try:
            res = bx24.callMethod("crm.deal.get", id=dealID)
            return res
        except BitrixError as e:
            LOGGER.error('BX24 get deal::exception: ', extra={"e": e})
            return None

    @staticmethod
    def get_fields():
        try:
            res = bx24.callMethod("crm.deal.fields")
            return res
        except BitrixError as e:
            LOGGER.error('BX24 get_fields deal::exception: ', extra={"e": e})
            return None

    @staticmethod
    def insert(fields):
        try:
            id = bx24.callMethod("crm.deal.add", fields=fields,
                                 params={"REGISTER_SONET_EVENT": "Y"})
            return Deal.get(id)
        except BitrixError as e:
            LOGGER.error('BX24 insert deal::exception: ', extra={"e": e,"input fields":fields})
            return None

    @staticmethod
    def update(data_fields):
        # xu ly haravan_request de pass data vao fields
        try:
            id = data_fields.get("ID")
            res = bx24.callMethod("crm.deal.update", id=id, fields=data_fields)
            LOGGER.info('BX24 update_deal: ', extra={"res": res})
            return Deal.get(id)
        except Exception as e:
            LOGGER.error('BX24 update deal::exception: ', extra={"e": e,"data_fields":data_fields})
            return None

    @staticmethod
    def delete(id):
        try:
            res = bx24.callMethod("crm.deal.delete", id=id)
            LOGGER.info(f'delete_deal: {id} ', extra={"res": res})
            return True
        except Exception as e:
            LOGGER.error(f'delete_deal {id} ::exception: ', extra={"e": e})
            return False


class Product():

    
    @staticmethod
    def list():
        res = bx24.callMethod('crm.product.list')
        return res

    @staticmethod
    def listWithFilter(filter={}):
        res = bx24.callMethod('crm.product.list', filter=filter)
        return res

    @staticmethod
    def get(id):
        res = bx24.callMethod("crm.product.get", id=id)
        # print(res)
        return res

    @staticmethod
    def get_fields():
        res = bx24.callMethod("crm.product.fields")
        return res

    @staticmethod
    def insert(fields):
        try:
            id = bx24.callMethod("crm.product.add", fields=fields)
            return Product.get(id)
        except BitrixError as e:
            LOGGER.error('Product::insert::exception: ', extra={"e": e,"fields":fields})
            return None

    @staticmethod
    def update(data_fields):
        # xu ly haravan_request de pass data vao fields
        try:
            res = bx24.callMethod("crm.product.update", id=data_fields.get("ID"), fields=data_fields)
            LOGGER.info('Product:update: ', extra={"res": res})
            return Product.get(data_fields.get("ID"))
        except Exception as e:
            LOGGER.error('Product::update::exception: ', extra={"e": e,"data_fields":data_fields})
            return None

    @staticmethod
    def delete(id):
        try:
            res = bx24.callMethod("crm.product.delete", id=id)
            LOGGER.info('Product::delete: ', extra={"res": res})
            return True
        except Exception as e:
            LOGGER.error(f'Product::delete::exception: ID={id} ', extra={"e": e})
            return False


class DealProductRow():

    @staticmethod
    def get(fields):
        try:
            res = bx24.callMethod("crm.deal.productrows.get", fields=fields)
            return res
        except BitrixError as e:
            LOGGER.error('Productrows::get::exception: ', extra={"error": e, 'fields input':fields })
            return None

    @staticmethod
    def set(data_fields):
        # xu ly haravan_request de pass data vao fields
        try:
            res = bx24.callMethod("crm.deal.productrows.set", **data_fields)
            LOGGER.info('ProductRow:update: ', extra={"res": res})
            return DealProductRow.get(data_fields.get("ID"))
        except Exception as e:
            LOGGER.error('Product::update::exception: ', extra={"e": e, "data_fields":data_fields})
            return None


class Contact():

    @staticmethod
    def list():
        res = bx24.callMethod('crm.contact.list',
                              select=["*", "UF_*", "PHONE", "EMAIL"])  # Lay cac thong tin ma list bi han che
        return res

    @staticmethod
    def get(id):
        res = bx24.callMethod("crm.contact.get", id=id)
        # print(res)
        return res

    @staticmethod
    def get_fields():
        res = bx24.callMethod("crm.contact.fields")
        return res

    @staticmethod
    def insert(fields):
        try:
            id = bx24.callMethod("crm.contact.add", fields=fields, params={"REGISTER_SONET_EVENT": "Y"})
            res = Contact.get(id)
            return res
        except BitrixError as e:
            LOGGER.error('Contact::insert::exception: ', extra={"e": e,"fields":fields})
            return None

    @staticmethod
    def update(data_fields):
        # xu ly haravan_request de pass data vao fields
        try:
            LOGGER.info('Contact:update: ', extra={"id": id})
            result = bx24.callMethod("crm.contact.update", id=data_fields.get("ID"), fields=data_fields)
            if result:
                return Contact.get(data_fields.get("ID"))
        except Exception as e:
            LOGGER.error('Contact::update::exception: ', extra={"e": e,"data_fields":data_fields})
            return None

    @staticmethod
    def delete(id):
        try:
            res = bx24.callMethod("crm.contact.delete", id=id)
            LOGGER.info('Contact::delete: ', extra={"res": res})
            return True
        except Exception as e:
            LOGGER.error(f'Contact::delete::exception: ID={id}', extra={"e": e})
            return False


# lay product by deal id
def getProductByDealID(dealID):
    res = bx24.callMethod("crm.deal.productrows.get", id=dealID)
    print(res)


# # # # # # # # # # # # # # # CONTACT FUNCTIONS # # # # # # # # # # # # # # #

# lay contact by id
def getContactByID(contactID):
    print(contactID)
    res = bx24.callMethod("crm.contact.get", id=236901)
    return res


# lay contact id by phone
def getContactIDbyPhone(phone):
    res = bx24.callMethod("crm.contact.list", filter={"PHONE": "0915453110"})
    return res


class Catalog:

    @staticmethod
    def catalog_list():
        res = bx24.callMethod("crm.catalog.list")
        return res


# # # # # # # # # # # # # # # PRODUCT FUNCTIONS # # # # # # # # # # # # # # #

# # lay product list
# def getProductListToFile():
#     res = bx24.callMethod("crm.product.list")
#     common.writeFile(res, "crm.contact.list.json")


# res = bx24.callMethod("crm.catalog.list")
# res = bx24.callMethod("catalog.product.list",
#                       select=[
#                           "id",
#                           "iblockId",
#                           "name",
#                           "detailTextType",
#                           "height",
#                           "iblockSectionId",
#                           "length",
#                           "measure",
#                           "previewPicture",
#                           "previewText",
#                           "previewTextType",
#                           "purchasingCurrency",
#                           "purchasingPrice",
#                           "quantity",
#                           "sort",
#                           "weight",
#                           "vatIncluded",
#                           "weight",
#                           "width",
#
#                       ], filter={"iblockId": "25"})
#
#
# id = 25

# res = bx24.callMethod("crm.deal.productrows.get")
# res = Product.list()
# res = bx24.callMethod("catalog.product.add", fields={
#     "active":"Y",
#     "bundle":"N",
#     "canBuyZero":"Y",
#     "code":"t-shirt",
#     "createdBy":"1",
#     "dateActiveFrom":"2019-06-04T19:36:00+03:00",
#     "dateActiveTo":"2019-06-05T19:57:00+03:00",
#     "dateCreate":"2018-10-22T11:31:15+03:00",
#     "detailText":"\u041e\u0442\u043b\u0438\u0447\u043d\u0430\u044f \u0444\u0443\u0442\u0431\u043e\u043b\u043a\u0430",
#     "detailTextType":"html",
#     "iblockId":"25",
#     "iblockSectionId":"11",
#     "length":"123",
#     "measure":"5",
#     "modifiedBy":"1",
#     "name":"\u0424\u0443\u0442\u0431\u043e\u043b\u043a\u0430 \u0416\u0435\u043d\u0441\u043a\u0438\u0439 \u0421\u043e\u0431\u043b\u0430\u0437\u043d",
#     "previewText":"previewText",
#     "previewTextType":"text",
#     "purchasingCurrency":"USD",
#     "purchasingPrice":"1000",
#     "quantity":"100",
#     "quantityReserved":"1",
#     "quantityTrace":"N",
#     "sort":"340",
#     "subscribe":"Y",
#     "vatId":"1",
#     "vatIncluded":"Y",
#     "weight":"10",
#     "width":"20",
#     "xmlId":"bx123123",
#
# })
# res = bx24.callMethod("crm.deal.productrows.get", id="19")
# res = bx24.callMethod("crm.deal.list")
# res = bx24.callMethod("crm.deal.productrows.set", id="3301", rows=[
#     {
#         "PRODUCT_ID": 2189,
#         "PRICE": 2199000,
#         "QUANTITY": 1,
#         "MEASURE_CODE": 796,
#         "MEASURE_NAME": "pcs.",
#     }
# ])
# res = bx24.callMethod("crm.deal.productrows.set", id= "19",
#                                                        rows= {
#                                                            "0": { "PRODUCT_ID": 689, "PRICE": 100.00, "QUANTITY": 4 },
#                                                            "1": { "PRODUCT_ID": 690, "PRICE": 400.00, "QUANTITY": 1 },
#                                                        })
# print(json.dumps(res))
# res = bx24.callMethod("crm.product.list")
# res = bx24.callMethod("crm.deal.list")
# res = bx24.callMethod("crm.deal.get", id="25")
# res = bx24.callMethod("crm.deal.productrows.get", id="3301")
# res = bx24.callMethod("crm.productrow.fields")
# res = bx24.callMethod("catalog.section.getFields")
# res = bx24.callMethod("catalog.section.list",filter={"iblockId": 25})
# res = bx24.callMethod("crm.deal.userfield.list")
# res = bx24.callMethod("crm.deal.userfield.get", id="201")
# fields={}
# fields["CONTACT_ID"] = 443
# fields["STAGE_ID"] = "NEW"
# fields["TITLE"] = "TITLE"
# fields['CURRENCY_ID'] = "VND"
# fields["UF_CRM_1637252157269"] = "TEST"
# fields = {
#     'TITLE': 'Haravan Order 100000',
#     'ADDITIONAL_INFO': 'Customer contacted us about a custom engraving on this iPod',
#     # 'OPPORTUNITY': 1134000,
#     'CURRENCY_ID': 'VND',
#     # 'IS_MANUAL_OPPORTUNITY': 'N',
#     # 'STAGE_SEMANTIC_ID': 'P',
#     'CONTACT_ID': 445,
#     'STAGE_ID': 'NEW',
#     'UF_CRM_1637252157269': '1236239555'
# }
# res = bx24.callMethod("crm.deal.add", fields=fields)


# print(json.dumps(res))

# Deal.update({"ID": 104, "ADDITIONAL_INFO": "12345"})

# print(json.dumps(Contact.get_fields()))
# print(json.dumps(Contact.get(18290)))
