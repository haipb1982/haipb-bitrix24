import requests
import json

url = 'https://apis.haravan.com/com/customers.json'
my_headers = {'Authorization': 'Bearer 64DAB7780429D201D87D99BEA745223EA9116C3A10AD9EB3FCE817C5FF0912C4'}
def getBluOrders():
   
    response = requests.get(url, headers=my_headers)
    print(response.json())
    return response

def getBluProducts():
    
    response = requests.get(url, headers=my_headers)
    print(response.json())
    return response

# GET https://apis.haravan.com/com/customers.json
def getBluCustomers():
    
    response = requests.get(url, headers=my_headers)
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

    res = getBluCustomers()
    writeFile(res.json(),'blu-customers.json')
    pass