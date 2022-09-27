from flask import Flask, request
from python_code.utils import get_convert_currency
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p><b>Hello, World!</b></p>"


@app.route("/rates", methods=['GET'])
def get_rates():
    date = request.args.get('date', default='24.04.2020')
    base_currency = request.args.get('base_currency', default='UAH')
    exchange_currency = request.args.get('exchange_currency', default='UAH')
    source = request.args.get('source', default='NB')
    result = get_convert_currency(date, base_currency,
                                  exchange_currency, source)
    return f'<p>{result}</p>'
