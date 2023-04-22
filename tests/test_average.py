import pytest
from app import app
from resources.shared import VALID_CURRENCIES_A, ERROR_CURRENCY_CODE, ERROR_NO_DATA, ERROR_DATE_FORMAT

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_average_basic(client):
    response = client.get("/average/USD/2023-04-20")
    assert response.status_code == 200
    assert response.json["mid"] == 4.2024

def test_average_weekend(client):
    response = client.get("/average/USD/2023-04-22")
    assert response.status_code == 404
    assert response.json["error"] == ERROR_NO_DATA

def test_average_holiday(client):
    response = client.get("/average/USD/2022-01-06")
    assert response.status_code == 404
    assert response.json["error"] == ERROR_NO_DATA

def test_average_date_range(client):
    """
    note: test valid until 21.04.2099
    """
    #valid date
    response = client.get("/average/USD/2022-04-20")
    assert response.status_code == 200

    #past date
    response = client.get("/average/USD/1999-04-20")
    assert response.json["error"] == ERROR_NO_DATA

    #future date
    response = client.get("/average/USD/2099-04-20")
    assert response.status_code != 200

def test_average_currencies(client):
    #supported currencies
    for currency in VALID_CURRENCIES_A:
        response = client.get(f"/average/{currency}/2022-04-20")
        assert response.status_code == 200
    
    #different letter cases
    response = client.get(f"/average/USD/2022-04-20")
    assert response.status_code == 200
    response = client.get(f"/average/uSd/2022-04-20")
    assert response.status_code == 200

    #unsupported currency
    response = client.get(f"/average/222/2022-04-20")
    assert response.json["error"] == ERROR_CURRENCY_CODE

    response = client.get(f"/average/PLN/2022-04-20")
    assert response.json["error"] == ERROR_CURRENCY_CODE

    response = client.get(f"/average/abcd/2022-04-20")
    assert response.json["error"] == ERROR_CURRENCY_CODE


def test_average_input_format(client):
    #regular date
    response = client.get(f"/average/USD/2022-04-20")
    assert response.status_code == 200

    #shortened date
    response = client.get(f"/average/USD/2022-3-8")
    assert response.status_code == 200

    #invalid dates
    response = client.get(f"/average/USD/2022-03-32")
    assert response.json["error"] == ERROR_DATE_FORMAT
    response = client.get(f"/average/USD/2022-20-04")
    assert response.json["error"] == ERROR_DATE_FORMAT

    #incorrect input
    response = client.get(f"/average/2022-20-04/USD")
    assert response.status_code != 200
    response = client.get(f"/average/USD")
    assert response.status_code != 200
    response = client.get(f"/average//2022-20-04")
    assert response.status_code != 200