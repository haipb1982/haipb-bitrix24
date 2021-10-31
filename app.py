from calendar import mdays
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import json
import bx24
import bx24 as Bx24
from dao import deal_dao

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to HAIPB1982 APIs</h1>"

@app.route('/webhooks', methods=['GET', 'POST'])
def webhooks():
    print(request.headers)
    body = request.get_json()
    print("BODY: ", body)
    headers = request.headers
    # if id != '1236954857':
    #     return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    topic = headers.get("x-haravan-topic")
    today = datetime.now()
    next_month_of_today = today + timedelta(mdays[today.month])

    if topic == 'orders/create':
        haravanOrderId = body.get("id")
        haravan_order = deal_dao.getHaravanID(haravanOrderId)
        print(haravan_order)
        if haravan_order :
            return json.dumps({'success':False, "message": "Dữ liệu đã tồn tại"}), 200, {'ContentType':'application/json'}
        fields = {
            "TITLE": body.get("name"),
            "ADDITIONAL_INFO": body.get("note"),
            "OPPORTUNITY": body.get("total_price"),
            "STAGE_ID": "NEW",
            # "CURRENCY_ID": "VND",
            "BEGINDATE": today,
            "CLOSEDATE": next_month_of_today
        }
        bitrix24_id = bx24.addNewDeal(fields)
        result = deal_dao.addNewDeal(hanravan_id=haravanOrderId, bitrix24_id=bitrix24_id, note="")
        if result:
            return json.dumps({'success':True, "message": "Thêm dữ liệu thành công"}), 200, {'ContentType':'application/json'}

    elif topic == 'orders/updated':
        haravanOrderId = body.get("id")
        haravan_order = deal_dao.getHaravanID(haravanOrderId)
        print(haravan_order)
        # Nếu đã có dữ liệu thì sẽ cập nhật còn nếu ko thì sẽ tạo mới rồi lưu vào database
        # TODO : Sẽ làm tạo mới nếu ko tìm thấy sau
        if haravan_order :
            fields = {
                "ID": haravan_order[2],
                "TITLE": body.get("name"),
                "ADDITIONAL_INFO": body.get("note"),
                "OPPORTUNITY": body.get("total_price"),
            }
            result = bx24.updateDeal(fields)
            if result:
                return json.dumps({'success':True, "message": "Cập nhật dữ liệu thành công"}), 200, {'ContentType':'application/json'}

    elif topic == 'orders/paid':
        haravanOrderId = body.get("id")
        haravan_order = deal_dao.getHaravanID(haravanOrderId)
        if haravan_order :
            fields = {
                "ID": haravan_order[2],
                "STAGE_ID": "FINAL_INVOICE", # Trạng thái sẽ lấy từ dealcategory_stage.json -> Cần xác định trạng thái của hệ thống vì nó là dynamic
            }
            result = bx24.updateDeal(fields)
            if result:
                return json.dumps({'success':True, "message": "Cập nhật dữ liệu thành công"}), 200, {'ContentType':'application/json'}
    elif topic == 'orders/cancelled':
        haravanOrderId = body.get("id")
        haravan_order = deal_dao.getHaravanID(haravanOrderId)
        if haravan_order :
            fields = {
                "ID": haravan_order[2],
                "STAGE_ID": "LOSE",
            }
            result = bx24.updateDeal(fields)
            if result:
                return json.dumps({'success':True, "message": "Cập nhật dữ liệu thành công"}), 200, {'ContentType':'application/json'}
    elif topic == 'orders/fulfilled':
        haravanOrderId = body.get("id")
        haravan_order = deal_dao.getHaravanID(haravanOrderId)
        if haravan_order :
            fields = {
                "ID": haravan_order[2],
                "STAGE_ID": "WON",
            }
            result = bx24.updateDeal(fields)
            if result:
                return json.dumps({'success':True, "message": "Cập nhật dữ liệu thành công"}), 200, {'ContentType':'application/json'}
    elif topic == 'orders/delete':
        haravanOrderId = body.get("id")
        haravan_order = deal_dao.getHaravanID(haravanOrderId)
        if haravan_order :
            fields = {
                "ID": haravan_order[2]
            }
            result = bx24.deleteDeal(fields)
            if result:
                return json.dumps({'success':True, "message": "Cập nhật dữ liệu thành công"}), 200, {'ContentType':'application/json'}

    return json.dumps({'success':False}), 200, {'ContentType':'application/json'}

@app.route('/api/v1/bitrix24/webhooks/deal', methods=['GET', 'POST'])
def webhook_deal():

    _form = request.form
    _dealID = _form['data[FIELDS][ID]']
    _data = Bx24.getDeal(_dealID)

    print(f'bitrix24 _form:', _form)
    print(f'data[FIELDS][ID]: DEAL ID', _dealID)
    print(f'get deal detail ', _data)

    return {'message': '/api/v1/bitrix24/webhooks/deal done', 'data': _data}


endpoint = '/api/v1/bitrix24/'

@app.route(endpoint + 'orders/updated', methods=['GET', 'POST'])
def api_deal_updated():

    print('api_deal_updated')
    req = request.json
    Bx24.updateDeal(req)

    return {'message': endpoint + 'orders/updated'}

@app.route(endpoint + 'orders/create.json', methods=['GET', 'POST'])
def api_deal_create():

    print('api_deal_create')
    req = request.json
    # Bx24.createDeal(req)

    return {'message': endpoint + 'orders/create.json'}

@app.route(endpoint + 'orders/paid', methods=['GET', 'POST'])
def api_deal_paid():

    print('api_deal_paid')
    req = request.json
    # Bx24.paidDeal(req)

    return {'message': endpoint + 'orders/paid'}


@app.route(endpoint + 'orders/delete', methods=['GET', 'POST'])
def api_deal_delete():

    print('api_deal_delete')
    req = request.json
    # Bx24.deleteDeal(req)

    return {'message': endpoint + 'orders/delete'}

if __name__ == "__main__":
    deal_dao.initDB()
    app.run(host="localhost", port=5500, use_reloader=True)
