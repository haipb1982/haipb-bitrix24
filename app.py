from calendar import mdays
from datetime import datetime, timedelta

from flask import Flask, request

import bx24 as Bx24
from dao import deal_dao
from services import haravan_to_bitrix
from utils import log
from utils.common import build_response_200

LOGGER = log.get_logger(__name__)

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Welcome to HAIPB1982 APIs</h1>"


@app.route('/webhooks', methods=['GET', 'POST'])
def webhooks():
    body = request.get_json()
    headers = request.headers
    LOGGER.info("REQUEST: ", extra={"headers": headers, "body": body})
    # if id != '1236954857':
    #     return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    topic = headers.get("x-haravan-topic")

    today = datetime.now()
    next_month_of_today = today + timedelta(mdays[today.month])
    LOGGER.info("TIME: ", extra={"today": today})

    if topic == 'orders/create':
        result, status = haravan_to_bitrix.create_deal_bitrix(body)
        if status:
            return build_response_200("Thêm dữ liệu thành công")
        else:
            return build_response_200("Dữ liệu đã tồn tại")

    # Nếu đã có dữ liệu thì sẽ cập nhật còn nếu ko thì sẽ tạo mới rồi lưu vào database
    if topic == 'orders/updated':
        result, status = haravan_to_bitrix.update_deal_bitrix(body)
        if status:
            return build_response_200("Cập nhật dữ liệu thành công")
        else:
            return build_response_200("Cập nhật dữ liệu không thành công")

    elif topic == 'orders/paid':
        result, status = haravan_to_bitrix.paid_deal_bitrix(body)
        if status:
            return build_response_200("Cập nhật dữ liệu thành công")
        else:
            return build_response_200("Cập nhật dữ liệu không thành công")

    elif topic == 'orders/cancelled':
        result, status = haravan_to_bitrix.cancelled_deal_bitrix(body)
        if status:
            return build_response_200("Cập nhật dữ liệu thành công")
        else:
            return build_response_200("Cập nhật dữ liệu không thành công")

    elif topic == 'orders/fulfilled':
        result, status = haravan_to_bitrix.fulfilled_deal_bitrix(body)
        if status:
            return build_response_200("Cập nhật dữ liệu thành công")
        else:
            return build_response_200("Cập nhật dữ liệu không thành công")

    elif topic == 'orders/delete':
        id = body.get("id")
        result, status = haravan_to_bitrix.delete_deal_bitrix(id)
        if status:
            return build_response_200("Xóa dữ liệu thành công")
        else:
            return build_response_200("Xóa dữ liệu không thành công")

    return build_response_200()


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
