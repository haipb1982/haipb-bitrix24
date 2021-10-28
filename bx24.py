import json
import requests
from bitrix24 import *
from datetime import datetime

bx24 = Bitrix24('https://blusaigon.bitrix24.com/rest/2069/pc3dgsz0s0ohfz6v/crm.deal.list.json')

deal = { 
         'TITLE': 'HAIPB TEST DEAL 2', 'TYPE_ID': '', 'STAGE_ID': "C18:NEW", 'PROBABILITY': '', 'CURRENCY_ID': 'VND', 'OPPORTUNITY': 686868, 'IS_MANUAL_OPPORTUNITY': 'N', 'TAX_VALUE': '', 'LEAD_ID': '', 'COMPANY_ID': '0', 'CONTACT_ID': 236901, 'QUOTE_ID': '', 'BEGINDATE': datetime.now(), 'CLOSEDATE': datetime.now(), 'ASSIGNED_BY_ID': 1, 'CREATED_BY_ID': 7, 'MODIFY_BY_ID': 7, 'DATE_CREATE': datetime.now(), 'DATE_MODIFY': datetime.now(), 'OPENED': 'N', 'CLOSED': 'N', 'COMMENTS': '', 'ADDITIONAL_INFO': '', 'LOCATION_ID': '', 'CATEGORY_ID': 18, 'STAGE_SEMANTIC_ID': 'P', 'IS_NEW': 'Y', 'IS_RECURRING': 'N', 'IS_RETURN_CUSTOMER': 'N', 'IS_REPEATED_APPROACH': 'N', 'SOURCE_ID': '', 'SOURCE_DESCRIPTION': '', 'ORIGINATOR_ID': 33, 'ORIGIN_ID': 34, 'UTM_SOURCE': 35, 'UTM_MEDIUM': 36, 'UTM_CAMPAIGN': 37, 'UTM_CONTENT': 38, 'UTM_TERM': 39, 'UF_CRM_1626419521': 40, 'UF_CRM_1626419645': 41, 'UF_CRM_1626419711': 42, 'UF_CRM_1626419773': 43, 'UF_CRM_60FE433E3FBFC': 44, 'UF_CRM_60FE433E5FD29': 45, 'UF_CRM_1629079188': 46, 'UF_CRM_1627457986': 47, 'UF_CRM_1627606315': 48, 'UF_CRM_1627873425': 49, 'UF_CRM_1627873492': 50, 'UF_CRM_1627875523': 51, 'UF_CRM_1627875873': 52, 'UF_CRM_1628132442': 53, 'UF_CRM_1628132482': 54, 'UF_CRM_1628131833': 55, 'UF_CRM_1628155141': 56, 'UF_CRM_HANA_LEAD_ID': 57, 'UF_CRM_HANA_DEAL_ID': 58, 'UF_CRM_HANA_CHAT_URL': 59, 'UF_CRM_5F7C716902967': 60, 'UF_CRM_1623725469652': 61, 'UF_CRM_1623809034975': 62, 'UF_CRM_1628149922667': 63, 'UF_CRM_1628149948721': 64, 'UF_CRM_1628149984252': 65, 'UF_CRM_1629336877': 66, 'UF_CRM_61208953B806D': 67, 'UF_CRM_1630139611544': 68, 'UF_CRM_1630143314980': 69, 'UF_CRM_1630143954760': 70, 'UF_CRM_1630416306053': 71, 'UF_CRM_1630417157521': 72, 'UF_CRM_1630417292478': 73, 'UF_CRM_1630467922601': 74, 'UF_CRM_1630467958625': 75, 'UF_CRM_1630721600380': 76
        }

def getDealList():
    print(bx24.callMethod('crm.deal.list'))

def addNewDeal():
    try:
        id = bx24.callMethod("crm.deal.add", fields = deal,
            params = { "REGISTER_SONET_EVENT": "Y" }	)

        res = bx24.callMethod("crm.deal.get", id = id )
        print(res)

    except BitrixError as message:
        print(message)
    
    # get deal details by ID
    res = bx24.callMethod("crm.deal.get", id = 3255 )
    print(res)

# lay product by deal id
def getProductByDealID():
    res = bx24.callMethod("crm.deal.productrows.get", id = 3255 )
    print(res)

# lay contact by id
def getContactByID(id):
    print(id)
    res = bx24.callMethod("crm.contact.get", id = 236901 )
    return res

# lay contact id by phone
def getContactIDbyPhone():
    res = bx24.callMethod("crm.contact.list", filter = { "PHONE": "0915453110" })
    print(res)

# lay product list
def getProductListToFile():
    res = bx24.callMethod("crm.product.list")
    writeFile(res,"crm.contact.list.json")

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

def getBluProducts():
    url = 'https://apis.haravan.com/com/products.json'
    my_headers = {'Authorization': 'Bearer 64DAB7780429D201D87D99BEA745223EA9116C3A10AD9EB3FCE817C5FF0912C4'}
    
    response = requests.get(url, headers=my_headers)
    print(response.json())
    return response.json()

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

    getDealList()
    pass