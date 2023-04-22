# Root url for the NBP API
API_URL = "https://api.nbp.pl/api/"

# List of currencies accepted by NBP as of 2023-04-21
# https://nbp.pl/en/statistic-and-financial-reporting/rates/table-a/
# https://nbp.pl/en/statistic-and-financial-reporting/rates/table-c/
VALID_CURRENCIES_A = ["AUD","THB","BRL","BGN","CAD","CLP","CZK","DKK","EUR","HUF","HKD","UAH","ISK","INR","MYR","MXN","ILS","NZD","NOK","PHP","GBP","ZAR","RON","IDR","SGD","SEK","CHF","TRY","USD","KRW","JPY","CNY","XDR" ]
VALID_CURRENCIES_C = ["AUD","CAD","CZK","DKK","EUR","HUF","NOK","GBP","SEK","CHF","USD","JPY","XDR"]

ERROR_CURRENCY_CODE = "Invalid currency code."
ERROR_DATE_FORMAT = "Incorrect date format, expected YYYY-MM-DD"
ERROR_DATE_RANGE = "Invalid currency code."
ERROR_NO_DATA = "Exchange rate data is not available for this date."