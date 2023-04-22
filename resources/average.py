import requests
from datetime import datetime
from flask_restful import Resource
from flask import jsonify, make_response
from resources.shared import API_URL, VALID_CURRENCIES_A, ERROR_CURRENCY_CODE, ERROR_DATE_FORMAT, ERROR_NO_DATA

class AverageRate(Resource):
    def get(self, date : str, currency : str):
        if not currency.upper() in VALID_CURRENCIES_A:
            return make_response(jsonify({"error": ERROR_CURRENCY_CODE}), 400)

        try:
            date_temp = datetime.strptime(date, "%Y-%m-%d")
            
            if date_temp.weekday() in [5,6]:
                return make_response(jsonify({"error": ERROR_NO_DATA}), 404)
            
            #ensure correct date string format
            date = date_temp.strftime("%Y-%m-%d")
        except:
            return make_response(jsonify({"error": ERROR_DATE_FORMAT}), 400)

        url = f"{API_URL}/exchangerates/rates/a/{currency}/{date}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return make_response(jsonify({"mid": data["rates"][0]["mid"]}), 200)
        elif response.status_code == 404:
            return make_response(jsonify({"error": ERROR_NO_DATA}), 404)
        else:
            return make_response(jsonify({"error": response.text}), 400)