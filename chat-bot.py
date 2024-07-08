### Step-1: Setting the Environment (Using Terminal).

# python -m venv chatbot_env
# source chatbot_env\Scripts\activate
# pip install flask pandas transformers


"""### Step-2: Load and Understand Your Data."""

import pandas as pd
import numpy as np

from get_data_from_intent import get_total_revenue, get_total_assets, get_income_change, get_net_income, \
    get_revenue_change, get_total_liabilities, get_cash_flow, get_revenue_to_assets_ratio, \
    get_income_to_liabilities_ratio, compare_revenue
from flask import Flask, request, jsonify, send_from_directory
from get_intent_entities import intent_entities

fiscal_data = pd.read_csv('fiscal_data_report.csv')

"""### Step-3: Flask Application"""
app = Flask(__name__)


# Define the routes
@app.route('/')
def home():
    return send_from_directory('', 'index.html')


@app.route('/query', methods=['POST'])
def query():
    data = request.json
    message = data.get('message')
    data = request.json
    query_type, company, years = intent_entities(message)
    company_1 = company[0]
    company_2 = ""
    year_1 = 2023
    if len(company) > 1:
        company_2 = company[1]
    if len(years) > 0:
        year_1 = years[0]
    if company_2:
        if year_1:
            print(query_type + " - " + company_1 + " - " + company_2 + " - " + str(year_1))
        else:
            print(query_type + " - " + company_1 + " - " + company_2)
    else:
        if year_1:
            print(query_type + " - " + company_1 + " - " + str(year_1))
        else:
            print(query_type + " - " + company_1)
    #company = data.get('company')
    #company_b = data.get('company_b', None)
    #year = data.get('year', None)

    if query_type == 'get_total_revenue':
        result = get_total_revenue(fiscal_data, company_1, year_1)
    elif query_type == 'calculate_revenue_change':
        result = get_revenue_change(fiscal_data, company_1)
    elif query_type == 'get_net_income':
        result = get_net_income(fiscal_data, company_1, year_1)
    elif query_type == 'get_income_change':
        result = get_income_change(fiscal_data, company_1)
    elif query_type == 'get_total_assets':
        result = get_total_assets(fiscal_data, company_1, year_1)
    elif query_type == 'get_total_liabilities':
        result = get_total_liabilities(fiscal_data, company_1, year_1)
    elif query_type == 'cash_flow':
        result = get_cash_flow(fiscal_data, company_1, year_1)
    elif query_type == 'calculate_revenue_to_assets':
        result = get_revenue_to_assets_ratio(fiscal_data, company_1, year_1)
    elif query_type == 'calculate_income_to_liabilities':
        result = get_income_to_liabilities_ratio(fiscal_data, company_1, year_1)
    elif query_type == 'compare_company_revenue':
        result = compare_revenue(fiscal_data, company_1, company_2, year_1)
    else:
        result = "Invalid query type"

    return jsonify({'result': result.to_dict() if isinstance(result, pd.DataFrame) else result})


if __name__ == '__main__':
    app.run(debug=True)
