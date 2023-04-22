import requests
from flask_restful import Resource
from flask import jsonify, make_response
from resources.shared import api_url, validate_currency, validate_range

class DifferenceRange(Resource):
    def get(self, currency : str, range : int):
        if not validate_currency(currency):
            return make_response(jsonify({'error': 'Invalid currency code.'}), 400)
        
        if not validate_range(range):
            return make_response(jsonify({'error': 'Invalid number of quotations'}), 400)
        
        url = f"{api_url}/exchangerates/rates/c/{currency}/last/{range}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result = {"diff_max": 0, "date":""}
            for rate in data['rates']:
                #ensure correct precision
                difference = round(rate['ask'] - rate['bid'],4)
                #spread can be negative on rare occasions
                if abs(difference) > abs(result['diff_max']):
                    result['diff_max'] = difference
                    result['date'] = rate['effectiveDate']

            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify({'error': response.text}), 400)