This is a repository for the [gdn-internship-2023](https://github.com/joaquinfilipic-dynatrace/gdn-internship-2023) backend test task.
API was made in Flask and supports the required endpoints.
All API endpoints have a set of unit tests written with pytest.
There is a swagger UI present.
Application and its tests are docker-compatible.

# Usage:

## Main API

The API can be started by installing its dependencies and running app.py

Using CMD/PowerShell:

```
git clone https://github.com/PazleoJGC/gdn-internship-task-2023.git
cd gdn-internship-task-2023
pip install -r requirements.txt
python app.py
```

When the api is active, Swagger UI can be accessed by navigating to http://127.0.0.1:5000/ (you should be redirected to http://127.0.0.1:5000/swagger/)

The endpoints can also be accessed manually. Endpoints and examples are listed in the Endpoints section.

## Tests

Tests are integrated with Visual Studio Code and can be ran ran from the [Testing] tab. They can also be launched by using
`pytest tests` or `python -m pytest tests` from the project's main directory.

## Docker

In CMD or PowerShell, use following commands:

`docker pull pazleojgc/gdn-internship-task-2023:1.0.1` to download the image

`docker run -d --name pazleo-api -p 5000:5000 pazleojgc/gdn-internship-task-2023:1.0.1` to load the image into a container. This is only required once. To start the container again, use `docker start pazleo-api`.

The API is now running can be accessed directly or with UI at http://127.0.0.1:5000/swagger/

To run tests in the container, connect to its terminal by typing `docker exec -it pazleo-api sh` in the command line. Once the terminal is connected, use `pytest tests` to run tests, and `exit` to leave the container.

Once done, use `docker stop pazleo-api` to shut down the container.


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

Response: {"mid": 4.2006}

## */minmax/{currency}/last/{num_days}
Used for getting the minimum and maximum average exchange rate for a currency {currency} over the period of {num_days} workdays.
- Accepted currency values are listed in [Table A](https://nbp.pl/en/statistic-and-financial-reporting/rates/table-a/)
- {num_days} is a number between 1 and 255 (inclusive)

Endpoint returns `mid_min`, `mid_max`, `date_min` and `date_max` values in json format.

Example: http://127.0.0.1:5000/minmax/USD/last/7

Response: (the values are changing day to day) `{ "date_max": "2023-04-17", "date_min": "2023-04-21", "mid_max": 4.2261, "mid_min": 4.2006}`

## */difference/{currency}/last/{num_days}
Used for getting the highest spread for currency {currency} over the period of {num_days} workdays.
- Accepted currency values are listed in [Table C](https://nbp.pl/en/statistic-and-financial-reporting/rates/table-c/)
- {num_days} is a number between 1 and 255 (inclusive)

Endpoint returns `diff_max` and `date` in json format.

Example: http://127.0.0.1:5000/difference/USD/last/90

Response: (the values are changing day to day) `{"date": "2023-02-17", "diff_max": 0.0896 }`