import json

from bitrix24 import *

from utils import log

LOGGER = log.get_logger(__name__)

# bx24 = Bitrix24('https://blusaigon.bitrix24.com/rest/2069/pc3dgsz0s0ohfz6v/crm.deal.fields.json')
# bx24 = Bitrix24('https://b24-0o3r9m.bitrix24.com/rest/1/34vvg27jk5appc39/profile.json') # TuanNA
bx24 = Bitrix24('https://b24-nd8219.bitrix24.vn/rest/1/cjgdujez4jbs6nch/profile.json')  # HaiPB


class Deal():

    @staticmethod
    def list():
        res = bx24.callMethod('crm.deal.list')
        return res

    @staticmethod
    def get(dealID):
        res = bx24.callMethod("crm.deal.get", id=dealID)
        return res

    @staticmethod
    def get_fields():
        res = bx24.callMethod("crm.deal.fields")
        return res

    @staticmethod
    def insert(fields):
        try:
            id = bx24.callMethod("crm.deal.add", fields=fields,
                                 params={"REGISTER_SONET_EVENT": "Y"})
            return Deal.get(id)
        except BitrixError as e:
            LOGGER.info('add_new_deal::exception: ', extra={"e": e})
            return None

    @staticmethod
    def update(data_fields):
        # xu ly haravan_request de pass data vao fields
        try:
            id = data_fields.get("ID")
            res = bx24.callMethod("crm.deal.update", id=id, fields=data_fields)
            LOGGER.info('update_deal: ', extra={"res": res})
            return Deal.get(id)
        except Exception as e:
            LOGGER.info('update_deal::exception: ', extra={"e": e})
            return None

    @staticmethod
    def delete(id):
        try:
            res = bx24.callMethod("crm.deal.delete", id=id)
            LOGGER.info('delete_deal: ', extra={"res": res})
            return True
        except Exception as e:
            LOGGER.info('delete_deal::exception: ', extra={"e": e})
            return False


class Product():

    @staticmethod
    def list():
        res = bx24.callMethod('crm.product.list')
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
            LOGGER.info('Product::insert::exception: ', extra={"e": e})
            return None

    @staticmethod
    def update(data_fields):
        # xu ly haravan_request de pass data vao fields
        try:
            res = bx24.callMethod("crm.product.update", id=data_fields.get("ID"), fields=data_fields)
            LOGGER.info('Product:update: ', extra={"res": res})
            return Product.get(data_fields.get("ID"))
        except Exception as e:
            LOGGER.info('Product::update::exception: ', extra={"e": e})
            return None

    @staticmethod
    def delete(id):
        try:
            res = bx24.callMethod("crm.product.delete", id=id)
            LOGGER.info('Product::delete: ', extra={"res": res})
            return True
        except Exception as e:
            LOGGER.info('Product::delete::exception: ', extra={"e": e})
            return False


class Contact():

    @staticmethod
    def list():
        res = bx24.callMethod('crm.contact.list')
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
            LOGGER.info('Contact::insert::exception: ', extra={"e": e})
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
            LOGGER.info('Contact::update::exception: ', extra={"e": e})
            return None

    @staticmethod
    def delete(id):
        try:
            res = bx24.callMethod("crm.contact.delete", id=id)
            LOGGER.info('Contact::delete: ', extra={"res": res})
            return True
        except Exception as e:
            LOGGER.info('Contact::delete::exception: ', extra={"e": e})
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


# # # # # # # # # # # # # # # PRODUCT FUNCTIONS # # # # # # # # # # # # # # #

# lay product list
def getProductListToFile():
    res = bx24.callMethod("crm.product.list")
    writeFile(res, "crm.contact.list.json")


# # # # # # # # # # # # # # # ULTIL FUNCTIONS # # # # # # # # # # # # # # #

# ghi file
def writeFile(res, filename):
    f = open(filename, "w+", encoding='utf-8')
    f.write(json.dumps(res))
    f.close()


def readJsonFile(filename):
    # data = {}
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

# Deal.update({"ID": 104, "ADDITIONAL_INFO": "12345"})