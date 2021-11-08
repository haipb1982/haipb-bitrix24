import requests
import json

from utils import log

LOGGER = log.get_logger(__name__)

url = 'https://apis.haravan.com/com/{}.json'
# blusaigon
# my_headers = {'Authorization': 'Bearer 64DAB7780429D201D87D99BEA745223EA9116C3A10AD9EB3FCE817C5FF0912C4'}
# haipb-haravan
my_headers = {'Authorization': 'Bearer AB75EDC1B3127319BD4C6237364CD2D7D742FCA8C18D9A577422CEDCE89BE9D8'}
token = "AB75EDC1B3127319BD4C6237364CD2D7D742FCA8C18D9A577422CEDCE89BE9D8"

class Order:

    @staticmethod
    def list():
        response = requests.get('https://apis.haravan.com/com/orders.json', headers=my_headers)
        return response.json()

    @staticmethod
    def get(id):
        response = requests.get('https://apis.haravan.com/com/orders/{}.json'.format(id), headers=my_headers)
        return response.json()

    @staticmethod
    def create(data):
        payload = {
            "order": {
                **data
            }
        }
        headers = {
            "Content-Type": "application/json",
            **my_headers
        }
        response = requests.post('https://apis.haravan.com/com/orders.json', headers=headers, data=json.dumps(payload))
        return response.json()

    # https://docs.haravan.com/support/solutions/articles/42000087683-orders
    # This operation allows for updating properties of an order including `shipping_address`, `note`, `tags`. It is not for editing the items of an order.
    @staticmethod
    def update(id, data):
        try:
            payload = {
                "order": {
                    "id": id,
                    **data
                }
            }
            headers = {
                "Content-Type": "application/json",
                **my_headers
            }
            response = requests.put('https://apis.haravan.com/com/orders/{}.json'.format(id), headers=headers, data=json.dumps(payload))
            return response.json().get("order")
        except Exception as e:
            LOGGER.error("Deal:update:exception: ", extra={"exception": e})
            return None

    @staticmethod
    def delete(id):
        try:
            headers = {
                "Content-Type": "application/json",
                **my_headers
            }
            requests.delete(f'https://apis.haravan.com/com/orders/{id}.json', headers=headers)
            return True
        except Exception as e:
            LOGGER.error("Product::delete:exception", extra={"exception": e})
            return False

class Product:

    @staticmethod
    def list():
        response = requests.get('https://apis.haravan.com/com/products.json', headers=my_headers)
        return response.json()

    @staticmethod
    def get(id):
        response = requests.get(f'https://apis.haravan.com/com/products/{id}.json', headers=my_headers)
        return response.json()

    @staticmethod
    def create(data):
        payload = {
                "product": {
                    **data
                }
            }
        headers = {
            "Content-Type": "application/json",
            **my_headers
        }
        response = requests.post(f'https://apis.haravan.com/com/products.json', headers=headers, data=json.dumps(payload))
        return response.json()

    @staticmethod
    def update(id, data):
        payload = {
            "product": {
                "id": id,
                **data
            }
        }
        headers = {
            "Content-Type": "application/json",
            **my_headers
        }
        response = requests.put(f'https://apis.haravan.com/com/products/{id}.json', headers=headers, data=json.dumps(payload))
        return response.json()

    @staticmethod
    def delete(id):
        try:
            headers = {
                "Content-Type": "application/json",
                **my_headers
            }
            requests.delete(f'https://apis.haravan.com/com/products/{id}.json', headers=headers)
            return True
        except Exception as e:
            LOGGER.error("Product::delete:exception", extra={"exception": e})
            return False

class Contact:

    @staticmethod
    def list():
        response = requests.get('https://apis.haravan.com/com/contacts.json', headers=my_headers)
        return response.json()

    @staticmethod
    def get(id):
        response = requests.get(f'https://apis.haravan.com/com/contacts/{id}.json', headers=my_headers)
        return response.json()

    @staticmethod
    def create(data):
        payload = {
            "customer": {
                **data
            }
        }
        headers = {
            "Content-Type": "application/json",
            **my_headers
        }
        response = requests.post(f'https://apis.haravan.com/com/customers.json', headers=headers, data=json.dumps(payload))
        return response.json()

    @staticmethod
    def update(id, data):
        payload = {
            "contact": {
                "id": id,
                **data
            }
        }
        headers = {
            "Content-Type": "application/json",
            **my_headers
        }
        response = requests.put(f'https://apis.haravan.com/com/contacts/{id}.json', headers=headers, data=json.dumps(payload))
        return response.json()

    @staticmethod
    def delete(id):
        try:
            headers = {
                "Content-Type": "application/json",
                **my_headers
            }
            requests.delete(f'https://apis.haravan.com/com/contacts/{id}.json', headers=headers)
            return True
        except Exception as e:
            LOGGER.error("Contact::delete:exception", extra={"exception": e})
            return False

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

    # res = getBluProducts()
    # writeFile(res.json(),'blu-products.json')

    # res = getBluOrders()
    # writeFile(res.json(),'blu-orders.json')
    # res = Order.get(1236239555)
    # print(json.dumps(res))
    #
    # res = Order.update(1236239555, {"note": "OKOKOKOKOKO"})
    # print(res)
    # products = Product.list()
    # product = products.get("products")[0]
    # print(product)
    # res = Order.create({"note": "OKOKOKOKOKO",     "line_items": [
    #     {
    #         "variant_id": product.get("variants")[0].get("id"),
    #         "quantity": 1
    #     }
    # ]})
    # print(res)

    print(Product.get(1036868200))
