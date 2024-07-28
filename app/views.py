from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from datetime import datetime
from app.api_calls import get_clients, get_invoices_in_time_period_set, create_invoice
from app.authorization import api_key_auth
from app.config import Config
from app.models import InvoiceData


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/invoice_dates')
def choose_invoice_dates():
    return render_template('enter_invoices_dates.html')


@app.route('/invoices', methods=['POST'])
def list_invoices():
    start_date = format_date(request.form['start_date'])
    end_date = format_date(request.form['end_date'])
    if not start_date or not end_date:
        return jsonify({"error": "Missing start_date or end_date"}), 400
    invoices = get_invoices_in_time_period_set(start_date, end_date)
    invoices_data = invoices['items']
    return render_template('invoices.html', response_data=invoices_data)


def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%-m/%-d/%Y')


@app.route('/clients', methods=['GET'])
def list_clients():
    clients = get_clients()
    clients_data = clients["items"]
    return render_template('clients.html', response_data=clients_data)


@app.route('/new_invoice')
def enter_invoice_details():
    return render_template('create_invoice_form.html', api_key=Config.api_key)


@app.route('/new_invoice_status', methods=['POST'])
def create_invoice_via_api():
    api_key = request.headers.get('api_key')
    print(api_key)
    if not api_key_auth(api_key):
        return jsonify({"error": "Unauthorized"}), 403

    try:
        data = request.json
        invoice = InvoiceData(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        result, status_code = create_invoice(data)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

