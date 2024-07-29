import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    api_key = os.getenv('API_KEY', 'your_api_key')
    secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
    jwt_secret_key = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key')
    jwt_access_token_expires = timedelta(hours=1)
    jwt_algorithm = os.environ.get('JWT_ALGORITHM', 'default_jwt_algorithm')
    client_id = os.getenv('NETSUITE_CLIENT_ID', 'your_client_id')
    client_secret = os.getenv('NETSUITE_CLIENT_SECRET', 'your_client_secret')
    redirect_uri = os.getenv('NETSUITE_REDIRECT_URI', 'your_redirect_uri')
    netsuite_username = os.getenv('NETSUITE_USERNAME', 'your_username')
    netsuite_password = os.getenv('NETSUITE_PASSWORD', 'your_password')
    netsuite_security_answer = os.getenv('NETSUITE_SECURITY_ANSWER', 'your_security_answer')
    account_id = os.getenv('NETSUITE_ACCOUNT_ID', 'your_account_id')
    refresh_token = os.getenv('NETSUITE_REFRESH_TOKEN', 'your_refresh_token')
    base_url = os.getenv('NETSUITE_BASE_URL_PART', 'your_base_url')
    query_url = os.getenv('NETSUITE_QUERY_URL_PART', 'your_query_url')
    invoices_url = os.getenv('NETSUITE_INVOICES_URL_PART', 'your_query_url')
    token_url = f"https://{account_id}.{base_url}/auth/oauth2/v1/token"
    auth_url = f"https://{account_id}.{base_url}/auth/oauth2/v1/authorize"
