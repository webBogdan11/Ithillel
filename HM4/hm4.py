from flask import Flask, request
import utils_db

app = Flask(__name__)


@app.route("/customers", methods=['GET'])
def customers():
    city = request.args.get('city', default=None)
    state = request.args.get('state', default=None)
    data = utils_db.get_filter_customers(city, state)
    return utils_db.pretty_print(data)


@app.route("/first_name", methods=['GET'])
def first_name():
    data = utils_db.get_first_name_count()
    return utils_db.pretty_print(data)


@app.route("/total_sum", methods=['GET'])
def total_sum():
    data = utils_db.get_total_sum()
    return utils_db.pretty_print(data)
