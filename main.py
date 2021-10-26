from flask import Flask, request, jsonify
try:
  import bx24 as Bx24
except:
  pass

app= Flask(__name__)

@app.route('/')
def home():
  return "<h1>Welcome to CodingX</h1>"

@app.route('/api/v1/bitrix24/webhooks/deal',methods=['GET', 'POST'])
def webhook_deal():

  _form = request.form
  print(f'bitrix24 _form:', _form)
  print(f'bitrix24 _form:', _form['data[FIELDS][ID]'])

  return { 'message': '/api/v1/bitrix24/webhooks/deal done'}

@app.route('/api/v1/bitrix24/get/deal',methods=['GET', 'POST'])
def api_get_deal():
  Bx24.getDealList()

  return { 'message': '/api/v1/bitrix24/get/deal done'}


if __name__ == "__main__":
  app.run(use_reloader=True)