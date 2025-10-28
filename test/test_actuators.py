import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.api.endpoints import actuators 
from app.main import app  

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_gpio():
    with patch.object(actuators, "gpio", autospec=True) as mock_gpio:
        yield mock_gpio

def test_watering_on(mock_gpio):
    response = client.post("/actuators/watering-on")
    assert response.status_code == 200
    assert response.json() == {"status": "Watering is ON"}
    mock_gpio.watering_on.assert_called_once()


def test_watering_off(mock_gpio):
    response = client.post("/actuators/watering-off")
    assert response.status_code == 200
    assert response.json() == {"status": "Watering is OFF"}
    mock_gpio.watering_off.assert_called_once()

def test_heating_on(mock_gpio):
    response = client.post("/actuators/heating-on")
    assert response.status_code == 200
    assert response.json() == {"status": "Heating is ON"}
    mock_gpio.heating_on.assert_called_once()

def test_heating_off(mock_gpio):
    response = client.post("/actuators/heating-off")
    assert response.status_code == 200
    assert response.json() == {"status": "Heating is OFF"}
    mock_gpio.heating_off.assert_called_once()


def test_led_strip_on(mock_gpio):
    payload = {"brightness": 3}
    response = client.post("/actuators/led-strip-on", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "LED strip is ON, level: 3"}
    mock_gpio.led_strip_on.assert_called_once_with(3)


def test_led_strip_off(mock_gpio):
    response = client.post("/actuators/led-strip-off")
    assert response.status_code == 200
    assert response.json() == {"status": "LED strip is OFF"}
    mock_gpio.led_strip_off.assert_called_once()


def test_roof_open_success(mock_gpio):
    response = client.post("/actuators/roof-open")
    assert response.status_code == 200
    assert response.json() == {"status": "Roof is OPEN"}
    mock_gpio.roof_open.assert_called_once()


def test_roof_close_success(mock_gpio):
    response = client.post("/actuators/roof-close")
    assert response.status_code == 200
    assert response.json() == {"status": "Roof is CLOSED"}
    mock_gpio.roof_close.assert_called_once()


def test_roof_open_failure(mock_gpio):
    mock_gpio.roof_open.side_effect = Exception("Servo error")
    response = client.post("/actuators/roof-open")
    assert response.status_code == 500
    assert "Servo error" in response.json()["detail"]


def test_atomiser_on(mock_gpio):
    response = client.post("/actuators/atomiser-on")
    assert response.status_code == 200
    assert response.json() == {"status": "Atomiser is ON"}
    mock_gpio.atomiser_on.assert_called_once()


def test_atomiser_off(mock_gpio):
    response = client.post("/actuators/atomiser-off")
    assert response.status_code == 200
    assert response.json() == {"status": "Atomiser is OFF"}
    mock_gpio.atomiser_off.assert_called_once()
