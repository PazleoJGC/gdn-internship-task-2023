This is a repository for the [gdn-internship-2023](https://github.com/joaquinfilipic-dynatrace/gdn-internship-2023) backend test tasks.
API was made in Flask and supports the required endpoints.
All API endpoints have a set of unit tests written with pytest.
There is a swagger UI present.
Application and its tests are docker-compatible.

# Usage:

## Main API

The API can be started by installing its dependencies and running app.py

```
pip install -r requirements.txt
python app.py
```

When the api is active, Swagger UI can be accessed by navigating to http://127.0.0.1:5000/swagger/

The endpoints can also be accessed manually. Endpoints and examples are listed in the Endpoints section.

## Tests

Tests are integrated with Visual Studio Code and can be ran ran from the [Testing] tab. They can also be launched by using
`pytest tests` or `python -m pytest tests` from the project's main directory.

## Docker

---

# Endpoints:

## */swagger
Swagger UI with all the API endpoints listed and documented.

## */average/{currency}/{date}
Used for getting the average exchange rate for a currency {currency} on the day {date}.
- Accepted currency values are listed in [Table A](https://nbp.pl/en/statistic-and-financial-reporting/rates/table-a/)
- Date should follow "YYYY-MM-DD" formatting

Endpoint returns a `mid` value in json format.

Example: http://127.0.0.1:5000/average/USD/2023-04-21

## */minmax/{currency}/last/{num_days}
Used for getting the minimum and maximum average exchange rate for a currency {currency} over the period of {num_days} workdays.
- Accepted currency values are listed in [Table A](https://nbp.pl/en/statistic-and-financial-reporting/rates/table-a/)
- {num_days} is a number between 1 and 255 (inclusive)

Endpoint returns `mid_min`, `mid_max`, `date_min` and `date_max` values in json format.

Example: http://127.0.0.1:5000/minmax/USD/last/7

## */difference/{currency}/last/{num_days}
Used for getting the highest spread for currency {currency} over the period of {num_days} workdays.
- Accepted currency values are listed in [Table C](https://nbp.pl/en/statistic-and-financial-reporting/rates/table-c/)
- {num_days} is a number between 1 and 255 (inclusive)

Endpoint returns `diff_max` and `date` in json format.

Example: http://127.0.0.1:5000/difference/USD/last/7