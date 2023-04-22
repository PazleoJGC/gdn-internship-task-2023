import pytest
from app import app
from resources.shared import VALID_CURRENCIES_B, ERROR_CURRENCY_CODE, ERROR_DATE_RANGE

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_difference_basic(client):
    response = client.get("/difference/USD/last/1")
    assert response.status_code == 200
    assert "diff_max" in response.json
    assert "date" in response.json

def test_difference_date_range(client):
    #too low
    response = client.get("/difference/USD/last/0")
    assert response.status_code == 400
    assert response.json["error"] == ERROR_DATE_RANGE

    #within range
    response = client.get("/difference/USD/last/1")
    assert response.status_code == 200
    response = client.get("/difference/USD/last/100")
    assert response.status_code == 200
    response = client.get("/difference/USD/last/255")
    assert response.status_code == 200

    #too high
    response = client.get("/difference/USD/last/256")
    assert response.status_code == 400
    assert response.json["error"] == ERROR_DATE_RANGE

def test_difference_input_format(client):
    #correct input
    response = client.get("/difference/USD/last/5")
    assert response.status_code == 200

    #incorrect input
    response = client.get("/difference/USD/last")
    assert response.status_code != 200
    response = client.get("/difference/USD/5")
    assert response.status_code != 200
    response = client.get("/difference/last/5/USD")
    assert response.status_code != 200
    response = client.get("/difference/5/last/USD")
    assert response.status_code != 200

def test_difference_currencies(client):
    #supported currencies
    for currency in VALID_CURRENCIES_B:
        print(currency)
        response = client.get(f"/difference/{currency}/last/5")
        assert response.status_code == 200
    
    #different letter cases
    response = client.get("/difference/USD/last/5")
    assert response.status_code == 200
    response = client.get("/difference/uSd/last/5")
    assert response.status_code == 200

    #unsupported currency
    response = client.get("/difference/123/last/5")
    assert response.json["error"] == ERROR_CURRENCY_CODE

    response = client.get("/difference/PLN/last/5")
    assert response.json["error"] == ERROR_CURRENCY_CODE

    response = client.get("/difference/abcd/last/5")
    assert response.json["error"] == ERROR_CURRENCY_CODE