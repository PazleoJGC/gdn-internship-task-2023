import requests
from datetime import datetime
from flask_restful import Resource
from flask import jsonify, make_response
from resources.shared import api_url, validate_currency

class AverageRate(Resource):
    def get(self, date : str, currency : str):
        if not validate_currency(currency):
            return make_response(jsonify({'error': 'Invalid currency code.'}), 400)

        try:
            date_temp = datetime.strptime(date, '%Y-%m-%d')
            if date_temp.weekday() in [5,6]:
                return make_response(jsonify({'error': "Exchange rate data is not available for this date."}), 404)
        except:
            return make_response(jsonify({'error': "Incorrect datetime format, expected YYYY-MM-DD"}), 400)

        url = f"{api_url}/exchangerates/rates/a/{currency}/{date}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return make_response(jsonify({'mid': data['rates'][0]['mid']}), 200)
        elif response.status_code == 404:
            return make_response(jsonify({'error': "Exchange rate data is not available for this date."}), 404)
        else:
            return make_response(jsonify({'error': response.text}), 400)