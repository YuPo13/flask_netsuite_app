import requests
import json
from app.authorization import get_netsuite_headers
from app.config import Config


def get_invoices_in_time_period_set(start_date: str, end_date: str):
    """
    This method retrieves invoices in time period requested
    :param start_date: invoices created starting from this date to be retrieved.
    :param end_date: invoices created up to (including) this date to be retrieved.
    :return: the list of invoices according to parameters set
    """
    headers = get_netsuite_headers()
    url = f"https://{Config.account_id}.{Config.base_url}{Config.query_url}"
    dated_query = (f"SELECT * FROM transaction, currency, entity WHERE transaction.currency = currency.id "
                   f"AND transaction.entity = entity.id AND transaction.recordtype='invoice' AND createddate>='{start_date}' "
                   f"AND createddate<='{end_date}'")
    query_body = json.dumps({"q": dated_query})
    response = requests.post(url, headers=headers, data=query_body)
    if response.status_code == 401:
        headers = get_netsuite_headers()
        response = requests.get(url, headers=headers)
    return response.json()


def get_clients():
    url = f"https://{Config.account_id}.{Config.base_url}{Config.query_url}"
    headers = get_netsuite_headers()
    query_body = json.dumps({"q": "SELECT * FROM customer"})
    response = requests.post(url, headers=headers, data=query_body)
    return response.json()


def create_invoice(data):
    """
    This method collects data entered by user at UI and creates a new invoice with minimum required fields in Netsuite.
    :param data: has a form of nested dictionary with the following input values:
    -> entity_id: ID of respective customer from Netsuite (i.e. it should exist in respective Netsuite listing).
    Has to be input as string, surrounded by quotation marks (e.g., "1341")
    -> location_id: ID of respective location from Netsuite (i.e. it should exist in respective Netsuite listing).
    Has to be input as string, surrounded by quotation marks (e.g., "6")
    -> item_id: ID of respective item from Netsuite (i.e. it should exist in respective Netsuite listing).
    Has to be input as string, surrounded by quotation marks (e.g., "252")
    -> item_cost: amount per 1 product/service item to be included into invoice. Has to be input as float (e.g., 5.0)
    -> item_quantity: quantity of product items to be included into invoice. Has to be input as integer (e.g., 8)

    Multiple items can be added into "items" list in the dictionary. Please make sure that the values of location id,
    entity id, item id already exist in Netsuite. Also please check if recent tax and posting periods are initiated
    in Netsuite

    :return: response status code 204 in case of successful payload posting
    """
    url = f"https://{Config.account_id}.{Config.base_url}{Config.invoices_url}"
    headers = get_netsuite_headers()
    try:
        response = requests.post(url, json=data, headers=headers)
        if (response.status_code == 200) or (response.status_code == 204):
            return "Success", response.status_code

        # Handle 4xx and 5xx status codes
        error_message = response.text
        if 400 <= response.status_code < 500:
            return {"error": f"Client error: {error_message}"}, response.status_code
        elif response.status_code >= 500:
            return {"error": f"Server error: {error_message}"}, response.status_code

    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}, 500
