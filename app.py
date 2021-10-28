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
    print(request.values)

    # print('api_deal_updated request:')
    # for item in request:
    #   print(item)

    # print('api_deal_updated request.values:')
    # for val in request.values:
    #   print(val)

    Bx24.updateDeal(3259)

    return {'message': endpoint + 'orders/updated'}


if __name__ == "__main__":
    app.run(use_reloader=True)
