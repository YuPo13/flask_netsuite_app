# Flask Netsuite Integration App

This is a simple Flask application that allows users to authorize and subsequently retrieve invoices data within the period requested, retrieve the customers data list and create new invoices.

## Requirements

- Python 3.6 or higher
- Flask and all dependencies listed in requirements.txt

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/YuPo13/flask_netsuite_app.git
   cd flask-invoice-app
   
2. Create a Virtual Environment

python -m venv venv

3. Activate the Virtual Environment

On Windows:
venv\Scripts\activate
On macOS and Linux:
source venv/bin/activate

4. Install the Dependencies
pip install -r requirements.txt


## Running the App

1. Add .env file with respective credentials values. It should be located in flask_netsuite_app folder.

2. Set the Flask Environment Variables. (Ignore this step if .env is already configured)

On Windows:
set FLASK_APP=run.py
set FLASK_ENV=development
On macOS and Linux:
export FLASK_APP=run.py
export FLASK_ENV=development

3. Run the Flask App in Terminal
flask run

4. Expected output in Terminal is as follows:
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 491-134-281

5. Open your web browser, go to http://127.0.0.1:5000 and follow proposed links


## Usage

Open your browser and navigate to http://127.0.0.1:5000. You will see a page with actions choice. It proposes you to:
1) login with your credentials. As of now no db is instantiated and for testing purposes a limited number of users are authorized.
2) obtain Netsuite transaction data (invoice record type) in requested time period. In order to do that follow the link "to retrieve the list of invoices from Netsuite", input respective time period start and end dates and push 'Submit' button. You'll be re-adressed to results page;
3) obtain customers' data. In order to do that follow the link "to retrieve the list of clients from Netsuite". You'll be re-adressed to results page;
4) create new invoice from UI proposed. In order to do that follow the link "to create a new invoice in Netsuite", follow instructions and input respective values: 
    -> entity_id: ID of respective customer from Netsuite (i.e. it should exist in respective Netsuite listing). Has to be input as string, surrounded by quotation marks (e.g., "1341")
    -> location_id: ID of respective location from Netsuite (i.e. it should exist in respective Netsuite listing). Has to be input as string, surrounded by quotation marks (e.g., "6")
    -> item_id: ID of respective item from Netsuite (i.e. it should exist in respective Netsuite listing). Has to be input as string, surrounded by quotation marks (e.g., "252")
    -> item_cost: amount per 1 product/service item to be included into invoice. Has to be input as float (e.g., 5.0)
    -> item_quantity: quantity of product items to be included into invoice. Has to be input as integer (e.g., 8)
Multiple items can be added into "items" list in the dictionary. Please make sure that the values of location id, entity id, item id already exist in Netsuite. Also please check if recent tax and posting periods are initiated in Netsuite.
After filling new invoice fields push "Submit" button and wait until the information message appear.