import pytest
from app import app
from resources.shared import VALID_CURRENCIES_A, ERROR_CURRENCY_CODE, ERROR_DATE_RANGE

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_minmax_basic(client):
    response = client.get("/minmax/USD/last/1")
    assert response.status_code == 200
    assert response.json["mid_min"] == response.json["mid_max"] 
    assert "mid_min" in response.json
    assert "mid_max" in response.json
    assert "date_min" in response.json
    assert "date_max" in response.json

def test_minmax_date_range(client):
    #too low
    response = client.get("/minmax/USD/last/0")
    assert response.status_code == 400
    assert response.json["error"] == ERROR_DATE_RANGE

    #within range
    response = client.get("/minmax/USD/last/1")
    assert response.status_code == 200
    response = client.get("/minmax/USD/last/100")
    assert response.status_code == 200
    response = client.get("/minmax/USD/last/255")
    assert response.status_code == 200

    #too high
    response = client.get("/minmax/USD/last/256")
    assert response.status_code == 400
    assert response.json["error"] == ERROR_DATE_RANGE

def test_minmax_input_format(client):
    #correct input
    response = client.get("/minmax/USD/last/5")
    assert response.status_code == 200

    #incorrect input
    response = client.get("/minmax/USD/last")
    assert response.status_code != 200
    response = client.get("/minmax/USD/5")
    assert response.status_code != 200
    response = client.get("/minmax/last/5/USD")
    assert response.status_code != 200
    response = client.get("/minmax/5/last/USD")
    assert response.status_code != 200

def test_minmax_currencies(client):
    #supported currencies
    for currency in VALID_CURRENCIES_A:
        response = client.get(f"/minmax/{currency}/last/5")
        assert response.status_code == 200
    
    #different letter cases
    response = client.get("/minmax/USD/last/5")
    assert response.status_code == 200
    response = client.get("/minmax/uSd/last/5")
    assert response.status_code == 200

    #unsupported currency
    response = client.get("/minmax/123/last/5")
    assert response.json["error"] == ERROR_CURRENCY_CODE

    response = client.get("/minmax/PLN/last/5")
    assert response.json["error"] == ERROR_CURRENCY_CODE

    response = client.get("/minmax/abcd/last/5")
    assert response.json["error"] == ERROR_CURRENCY_CODE