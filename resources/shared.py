# Root url for the NBP API
api_url = "https://api.nbp.pl/api/"

# List of currencies accepted by NBP as of 2023-04-21
# https://nbp.pl/en/statistic-and-financial-reporting/rates/table-a/
valid_currencies = [ "AUD","THB","BRL","BGN","CAD","CLP","CZK","DKK","EUR","HUF","HKD","UAH","ISK","INR","MYR","MXN","ILS","NZD","NOK","PHP","GBP","ZAR","RON","IDR","SGD","SEK","CHF","TRY","USD","KRW","JPY","CNY","XDR" ]

def validate_currency(currency_code : str) -> bool:
    """
    Returns true if currency code is on the list of currencies.
    
    Both uppercase and lowercase codes are accepted by NBP API
    """
    return currency_code.upper() in valid_currencies

def validate_range(range : int) -> bool:
    """
    Returns true if range is positive and below 256
    """
    return range > 0 and range < 256