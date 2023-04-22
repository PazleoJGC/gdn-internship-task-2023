import requests
from flask_restful import Resource
from flask import jsonify, make_response
from resources.shared import api_url, validate_currency, validate_range

class MinMaxLast(Resource):
    def get(self, currency : str, num_days : int):
        if not validate_currency(currency):
            return make_response(jsonify({'error': 'Invalid currency code.'}), 400)
        
        if not validate_range(num_days):
            return make_response(jsonify({'error': 'Invalid number of quotations'}), 400)

        url = f"{api_url}/exchangerates/rates/a/{currency}/last/{num_days}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result = {"mid_min": data['rates'][0]["mid"], "date_min":"", "mid_max": data['rates'][0]["mid"], "date_max":""}
            for rate in data['rates']:
                #if rates are equal, return the more recent one
                #recent values are at the end of the list

                if rate["mid"] >= result["mid_max"]:
                    result["mid_max"] = rate["mid"]
                    result["date_max"] = rate["effectiveDate"]

                if rate["mid"] <= result["mid_min"]:
                    result["mid_min"] = rate["mid"]
                    result["date_min"] = rate["effectiveDate"]

            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify({'error': response.text}), 400)
