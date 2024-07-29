from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.api_calls import get_clients, get_invoices_in_time_period_set, create_invoice
from app.authorization import api_key_auth
from app.config import Config
from app.models import InvoiceData, User
from app.user_credentials import USERS


app = Flask(__name__)
app.config.from_object(Config)
app.config["JWT_SECRET_KEY"] = Config.jwt_secret_key
app.config["SECRET_KEY"] = Config.secret_key
app.config["JWT_ALGORITHM"] = Config.jwt_algorithm

jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The token has expired. Please visit /login and enter your login and password again'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'status': 422,
        'msg': 'Invalid token'
    }), 422


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'status': 401,
        'msg': 'Request does not contain an access token'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'status': 401,
        'msg': 'Token has been revoked'
    }), 401


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        if USERS.get(username) == password:
            access_token = create_access_token(identity=username)
            response = jsonify(access_token=access_token)
            return response, 200
        else:
            flash('Invalid username or password.')
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"msg": "Logged out"}), 200


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
