from flask import Flask, request, jsonify
import bx24 as Bx24

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Welcome to HAIPB1982 APIs</h1>"


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

@app.route(endpoint + 'orders/create', methods=['GET', 'POST'])
def api_deal_create():

    print('api_deal_create')
    req = request.json
    # Bx24.createDeal(req)

    return {'message': endpoint + 'orders/create'}

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
    app.run(use_reloader=True)
