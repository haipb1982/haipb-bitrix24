import requests
import json

import simplejson

url = 'https://apis.haravan.com/com/{}.json'
# blusaigon
# my_headers = {'Authorization': 'Bearer 64DAB7780429D201D87D99BEA745223EA9116C3A10AD9EB3FCE817C5FF0912C4'}
# haipb-haravan
my_headers = {'Authorization': 'Bearer AB75EDC1B3127319BD4C6237364CD2D7D742FCA8C18D9A577422CEDCE89BE9D8'}
token = "AB75EDC1B3127319BD4C6237364CD2D7D742FCA8C18D9A577422CEDCE89BE9D8"

class Deal:

    @staticmethod
    def list():
        response = requests.get('https://apis.haravan.com/com/orders.json', headers=my_headers)
        return response.json()

    @staticmethod
    def get(id):
        response = requests.get('https://apis.haravan.com/com/orders/{}.json'.format(id), headers=my_headers)
        return response.json()

def getBluOrders():

    response = requests.get('https://apis.haravan.com/com/orders.json', headers=my_headers)
    print(response.json())
    return response

def getBluProducts():

    response = requests.get('https://apis.haravan.com/com/products.json', headers=my_headers)
    print(response.json())
    return response

# GET https://apis.haravan.com/com/customers.json
def getBluCustomers():

    response = requests.get('https://apis.haravan.com/com/customers.json', headers=my_headers)
    print(response.json())
    return response

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

# main
if __name__ == "__main__":
    print('rock!!!')
    # res = readJsonFile('blu-1order.json')
    # for  item in res :
    #         print(item)

    # res = getBluCustomers()
    # writeFile(res.json(),'blu-customers.json')

    # res = getBluOrders()
    # writeFile(res.json(),'blu-orders.json')
    res = Deal.get(1236239555)
    print(res)
    pass