import json
import time
from calendar import mdays
from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from flask_cors import CORS


import bx24 as Bx24
from dao import deal_dao, db
from services import haravan_to_bitrix, bitrix_to_haravan, webapp_service, retryjob_service
from utils import log
from utils.common import build_response_200, build_response_400, build_response_500

LOGGER = log.get_logger(__name__)

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "<h1>Welcome to HAIPB1982 APIs</h1>"


@app.route('/haravan/webhooks', methods=['GET', 'POST'])
def webhooks():
    body = request.get_json()
    headers = request.headers
    topic = headers.get("x-haravan-topic")

    LOGGER.info("/haravan/webhooks TOPIC: ", extra={"topic": topic})
    LOGGER.info("/haravan/webhooks REQUEST: ",
                extra={"headers": headers, "body": body})

    # if id != '1236954857':
    #     return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    # today = datetime.now()
    # next_month_of_today = today + timedelta(mdays[today.month])
    # LOGGER.info("TIME: ", extra={"today": today})

    haravanID = body.get('id',None)

    if topic == 'orders/create':
        status = haravan_to_bitrix.create_deal_bitrix(body)
        if status:
            return build_response_200("Thêm dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'ORDERS','CREATE')
            return build_response_200("Thêm dữ liệu không thành công")

    # Nếu đã có dữ liệu thì sẽ cập nhật còn nếu ko thì sẽ tạo mới rồi lưu vào database
    if topic == 'orders/updated':
        status = haravan_to_bitrix.update_deal_bitrix(body)
        if status:
            return build_response_200("Cập nhật dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'ORDERS','UPDATED')
            return build_response_200("Cập nhật dữ liệu không thành công")

    elif topic == 'orders/paid':
        status = haravan_to_bitrix.paid_deal_bitrix(body)
        if status:
            return build_response_200("Cập nhật dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'ORDERS','PAID')
            return build_response_200("Cập nhật dữ liệu không thành công")

    elif topic == 'orders/cancelled':
        status = haravan_to_bitrix.cancelled_deal_bitrix(body)
        if status:
            return build_response_200("Cập nhật dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'ORDERS','CANCELLED')
            return build_response_200("Cập nhật dữ liệu không thành công")

    elif topic == 'orders/fulfilled':
        status = haravan_to_bitrix.fulfilled_deal_bitrix(body)
        if status:
            return build_response_200("Cập nhật dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'ORDERS','FULFILLED')
            return build_response_200("Cập nhật dữ liệu không thành công")

    elif topic == 'orders/delete':
        id = body.get("id")
        status = haravan_to_bitrix.delete_deal_bitrix(id)
        if status:
            return build_response_200("Xóa dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'ORDERS','DELETE')
            return build_response_200("Xóa dữ liệu không thành công")

    elif topic == 'products/create':
        result = haravan_to_bitrix.create_product_bitrix(body)
        if result:
            return build_response_200("Thêm dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'PRODUCTS','CREATE')
            return build_response_200("Thêm dữ liệu không thành công")

    elif topic == 'products/update':
        result = haravan_to_bitrix.update_product_bitrix(body)
        if result:
            return build_response_200("Cập nhật dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'PRODUCTS','UPDATE')
            return build_response_200("Cập nhật dữ liệu không thành công")
    elif topic == 'products/delete':
        status = haravan_to_bitrix.deleted_product_bitrix(haravanID)
        if status:
            return build_response_200("Xóa dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'PRODUCTS','DELETE')
            return build_response_200("Xóa dữ liệu không thành công")
    elif topic == 'customers/create':
        result = haravan_to_bitrix.create_contact_bitrix(body)
        if result:
            return build_response_200("Thêm dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'CUSTOMERS','CREATE')
            return build_response_200("Thêm dữ liệu không thành công")

    elif topic == 'customers/update':
        status = haravan_to_bitrix.update_contact_bitrix(body)
        if status:
            return build_response_200("Cập nhật dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'CUSTOMERS','UPDATE')
            return build_response_200("Cập nhật dữ liệu không thành công")
    elif topic == 'customers/delete':
        status = haravan_to_bitrix.delete_contact_bitrix(haravanID)
        if status:
            return build_response_200("Xóa dữ liệu thành công")
        else:
            retryjob_service.insert(haravanID,body,None,None,'CUSTOMERS','DELETE')
            return build_response_200("Xóa dữ liệu không thành công")

    return build_response_200()


@app.route('/haravan-to-bitrix', methods=['GET', 'POST'])
def migrate_haravan_to_bitrix():
    haravan_customer = haravan_to_bitrix.migrate_customer_haravan_to_bitrix()
    haravan_product = haravan_to_bitrix.migrate_product_haravan_to_bitrix()
    haravan_order = haravan_to_bitrix.migrate_order_haravan_to_bitrix()
    return build_response_200()


@app.route('/bitrix/webhooks', methods=['GET', 'POST'])
def bitrix_webhooks():
    # return build_response_200()

    body = request.get_json()
    _form = request.form
    headers = request.headers
    LOGGER.info("REQUEST: ", extra={
                "headers": headers, "body": body, "form": _form})
    print(json.dumps(_form))

    event = _form.get("event")

    if not event:
        return build_response_200()

    ID = _form.get('data[FIELDS][ID]')

    if event == "ONCRMDEALADD":
        res = bitrix_to_haravan.create_order_haravan(ID)
    if event == "ONCRMDEALUPDATE":
        res = bitrix_to_haravan.update_order_haravan(ID)
    if event == "ONCRMPRODUCTDELETE":
        res = bitrix_to_haravan.delete_order_haravan(ID)

    if event == "ONCRMPRODUCTADD":
        res = bitrix_to_haravan.create_product_haravan(ID)
    if event == "ONCRMPRODUCTUPDATE":
        res = bitrix_to_haravan.update_product_haravan(ID)
    if event == "ONCRMPRODUCTDELETE":
        res = bitrix_to_haravan.delete_product_haravan(ID)

    if event == "ONCRMCONTACTADD":
        res = bitrix_to_haravan.create_contact_haravan(ID)
    if event == "ONCRMCONTACTUPDATE":
        res = bitrix_to_haravan.update_contact_haravan(ID)
    if event == "ONCRMCONTACTDELETE":
        res = bitrix_to_haravan.delete_contact_haravan(ID)

    if res:
        return build_response_200('Cập nhật Bitrix24 --> Haravan thành công')
    else:
        retryjob_service.insert(None,None,ID,None,event,event)
        return build_response_200('Cập nhật Bitrix24 --> Haravan thất bại!!!')

    return build_response_200()


# # # # # # # # # # # # # # # # # # # # # # # # # # #
# Các API cho webapp
# Moi trang 20 ket qua
__page_size = 20

@app.route('/api/v1/orders', methods=['GET'])
def webapp_get_all_orders():
    page = request.args.get("page")
    if page:
        res = webapp_service.get_all_orders_pages(
            int(page)*__page_size, (int(page)+1)*__page_size)
    else:
        res = webapp_service.get_all_orders()
    
    return jsonify(res)

@app.route('/api/v1/products', methods=['GET'])
def webapp_get_all_products():
    page = request.args.get("page")
    if page:
        res = webapp_service.get_all_products_pages(
            int(page)*__page_size, (int(page)+1)*__page_size)
    else:
        res = webapp_service.get_all_products()
    
    return jsonify(res)

@app.route('/api/v1/contacts', methods=['GET'])
def webapp_get_all_contacts():
    page = request.args.get("page")
    if page:
        res = webapp_service.get_all_contacts_pages(
            int(page)*__page_size, (int(page)+1)*__page_size)
    else:
        res = webapp_service.get_all_contacts()
    
    return jsonify(res)

@app.route('/api/v1/orders', methods=['POST'])
def webapp_order_actions():
    req = request.form

    action = req.get('action', None)
    __id =  req.get('id', None)
    haravan_id = req.get('haravan_id', None)
    bitrix24_id = req.get('bitrix24_id', None)

    res = {}

    if not action:
        res['code'] = 400
        res['message'] = 'No action found!'

    if action == 'delete':
        if not __id:
            res['code'] = 400
            res['message'] = 'DELETE record but wrong input data!'
        else:            
            res = webapp_service.delete_order_record(__id)

    if action == 'update':

        if not (__id and haravan_id and bitrix24_id):
            res['code'] = 400
            res['message'] = 'UPDATE record but wrong input data!'
        else:
            res = webapp_service.update_order_record(
                __id, haravan_id, bitrix24_id)

    if action == 'insert':
        if not( haravan_id and bitrix24_id):
            res['code'] = 400
            res['message'] = 'INSERT record but wrong data!'
        else:            
            res = webapp_service.insert_order_record(
                haravan_id, bitrix24_id)
    
    return jsonify(res)
    # if res['code'] == 400:
    #     return build_response_400(res['message'],res['data'])
    # elif res['code'] == 500:
    #     return build_response_500(res['message'],res['data'])
    # else:
    #     return build_response_200(res['message'],res['data'])

@app.route('/api/v1/products', methods=['POST'])
def webapp_product_actions():
    req = request.form

    action = req.get('action', None)
    __id =  req.get('id', None)
    haravan_id = req.get('haravan_id', None)
    bitrix24_id = req.get('bitrix24_id', None)

    res = {}

    if not action:
        res['code'] = 400
        res['message'] = 'No action found!'

    if action == 'delete':
        if not __id:
            res['code'] = 400
            res['message'] = 'DELETE record but wrong input data!'
        else:            
            res = webapp_service.delete_product_record(__id)

    if action == 'update':

        if not (__id and haravan_id and bitrix24_id):
            res['code'] = 400
            res['message'] = 'UPDATE record but wrong input data!'
        else:
            res = webapp_service.update_product_record(
                __id, haravan_id, bitrix24_id)

    if action == 'insert':
        if not( haravan_id and bitrix24_id):
            res['code'] = 400
            res['message'] = 'INSERT record but wrong input data!'
        else:            
            res = webapp_service.insert_product_record(
                haravan_id, bitrix24_id)
    
    return jsonify(res)


@app.route('/api/v1/contacts', methods=['POST'])
def webapp_contact_actions():
    req = request.form

    action = req.get('action', None)
    __id =  req.get('id', None)
    haravan_id = req.get('haravan_id', None)
    bitrix24_id = req.get('bitrix24_id', None)

    res = {}

    if not action:
        res['code'] = 400
        res['message'] = 'No action found!'

    if action == 'delete':
        if not __id:
            res['code'] = 400
            res['message'] = 'DELETE record but wrong input data!'
        else:            
            res = webapp_service.delete_contact_record(__id)

    if action == 'update':

        if not (__id and haravan_id and bitrix24_id):
            res['code'] = 400
            res['message'] = 'UPDATE record but wrong input data!'
        else:
            res = webapp_service.update_contact_record(
                __id, haravan_id, bitrix24_id)

    if action == 'insert':
        if not( haravan_id and bitrix24_id):
            res['code'] = 400
            res['message'] = 'INSERT record but wrong input data!'
        else:            
            res = webapp_service.insert_contact_record(
                haravan_id, bitrix24_id)
    
    return jsonify(res)

@app.route('/api/v1/sync', methods=['GET'])
def webapp_get_sync():
    type = request.args.get("type")
    id = request.args.get("id")
    res = {}
    if type and id:
        res = webapp_service.get_sync(type, id)
    else:
        res['code'] = 400
        res['message'] = 'SYNC data but wrong input data!'
    
    return jsonify(res)

# timer loop every 15 minutes
RETRY_JOBS_IN_MINUTES = 15
while True:
    print('retry_all_jobs!')
    retryjob_service.retry_all_jobs()
    time.sleep(RETRY_JOBS_IN_MINUTES*60)