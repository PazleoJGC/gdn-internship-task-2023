import requests
from flask_restful import Resource
from flask import jsonify, make_response
from resources.shared import API_URL, ERROR_CURRENCY_CODE, ERROR_DATE_RANGE, VALID_CURRENCIES_A

class MinMaxLast(Resource):
    def get(self, currency : str, num_days : int):
        """
        Returns minimum and maximum average exchange rate values, and the days they occured.
        
        Weekends and holidays are skipped and do not count towards the 'num_days' limit."
        """
        if not currency.upper() in VALID_CURRENCIES_A:
            return make_response(jsonify({"error": ERROR_CURRENCY_CODE}), 400)
        
        if not (num_days > 0 and num_days < 256):
            return make_response(jsonify({"error": ERROR_DATE_RANGE}), 400)

        url = f"{API_URL}/exchangerates/rates/a/{currency}/last/{num_days}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result = {"mid_min": data["rates"][0]["mid"], "date_min":"", "mid_max": data["rates"][0]["mid"], "date_max":""}
            for rate in data["rates"]:
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
            return make_response(jsonify({"error": response.text}), 400)
