from flask import Flask
import requests
from datetime import datetime, timedelta
from app.config import Config

app = Flask(__name__)

TOKEN_EXPIRY = "1970-01-01"
TOKEN_DATA = {'refresh_token': Config.refresh_token, 'access_token': None}


def get_new_access_token():
    global TOKEN_DATA, TOKEN_EXPIRY
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': TOKEN_DATA['refresh_token'],
        'client_id': Config.client_id,
        'client_secret': Config.client_secret,
    }
    response = requests.post(Config.token_url, data=payload)
    if response.status_code == 200:
        tokens = response.json()
        TOKEN_DATA['access_token'] = tokens['access_token']
        TOKEN_EXPIRY = datetime.now() + timedelta(seconds=int(tokens['expires_in']))
    else:
        raise Exception(f"Error refreshing token: {response.text}")


def get_netsuite_headers():
    if not TOKEN_DATA['access_token']: #or datetime.strptime(TOKEN_EXPIRY, "%Y-%m-%d") <= datetime.now()
        get_new_access_token()
    headers = {
        "Authorization": f"Bearer {TOKEN_DATA['access_token']}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Prefer": "transient",
        "x-api-key": Config.api_key
    }
    return headers


def api_key_auth(api_key):
    if api_key != Config.api_key:
        return False
    return True
