import requests
from flask_restful import Resource
from flask import jsonify, make_response
from resources.shared import API_URL, ERROR_CURRENCY_CODE, ERROR_DATE_RANGE, VALID_CURRENCIES_C

class DifferenceLast(Resource):
    def get(self, currency : str, num_days : int):
        """
        Returns the highest difference between "ask" and "bid" values, and the day it occured.
        
        Weekends and holidays are skipped and do not count towards the 'num_days' limit."
        """
        if not currency.upper() in VALID_CURRENCIES_C:
            return make_response(jsonify({"error": ERROR_CURRENCY_CODE}), 400)
        
        if not (num_days > 0 and num_days < 256):
            return make_response(jsonify({"error": ERROR_DATE_RANGE}), 400)
        
        url = f"{API_URL}/exchangerates/rates/c/{currency}/last/{num_days}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result = {"diff_max": 0, "date":""}
            for rate in data["rates"]:
                #ensure correct precision
                difference = round(rate["ask"] - rate["bid"],4)
                #spread can be negative on rare occasions
                if abs(difference) > abs(result["diff_max"]):
                    result["diff_max"] = difference
                    result["date"] = rate["effectiveDate"]

            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify({"error": response.text}), 400)