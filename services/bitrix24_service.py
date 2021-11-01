import json

from bitrix24 import *

from utils import log

LOGGER = log.get_logger(__name__)


bx24 = Bitrix24('https://blusaigon.bitrix24.com/rest/2069/pc3dgsz0s0ohfz6v/crm.deal.fields.json')
# bx24 = Bitrix24('https://b24-hfk65b.bitrix24.com/rest/1/ppyzdjwvsgune1od/crm.deal.fields.json') # TuanNA



def get_deals():
    res = bx24.callMethod('crm.deal.list')
    return res

def get_deal(dealID):
    res = bx24.callMethod("crm.deal.get", id=dealID)
    # print(res)
    return res

def get_fields():
    res = bx24.callMethod("crm.deal.fields")
    return res

def add_new_deal(fields):
    try:
        id = bx24.callMethod("crm.deal.add", fields = fields,
                             params = { "REGISTER_SONET_EVENT": "Y" }	)
        return id

    except BitrixError as e:
        LOGGER.info('add_new_deal::exception: ', extra={"e": e})
        return None


def update_deal(data_fields):
    # xu ly haravan_request de pass data vao fields
    try:
        res = bx24.callMethod("crm.deal.update", id = data_fields.get("ID") , fields = data_fields)
        LOGGER.info('update_deal: ', extra={"res": res})
        return True
    except Exception as e:
        LOGGER.info('update_deal::exception: ', extra={"e": e})
        return False

def delete_deal(id):
    try:
        res = bx24.callMethod("crm.deal.delete", id = id)
        LOGGER.info('delete_deal: ', extra={"res": res})
        return True
    except Exception as e:
        LOGGER.info('delete_deal::exception: ', extra={"e": e})
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
def getContactIDbyPhone(phone):
    res = bx24.callMethod("crm.contact.list", filter = { "PHONE": "0915453110" })
    return res

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

