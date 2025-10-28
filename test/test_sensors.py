import pytest
import requests
from datetime import datetime

BASE_URL = "http://192.168.1.16:8000"  

TEMP_MIN, TEMP_MAX = -10.0, 50.0
HUM_MIN, HUM_MAX = 0.0, 100.0
SOIL_MIN, SOIL_MAX = 0.0, 5.00
LIGHT_MIN, LIGHT_MAX = 0.0, 5.00

def test_read_live_conditions_success():
    response = requests.get(f"{BASE_URL}/sensors/read/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    record = data[0]

    expected_keys = {"id", "uid", "temp_1", "temp_2", "temp_3",
                     "humidity", "soil_humidity", "lighting", "date"}
    assert expected_keys == set(record.keys())

    for key in ["temp_1", "temp_2", "temp_3", "humidity", "soil_humidity", "lighting"]:
        assert isinstance(record[key], (float, int))

    assert TEMP_MIN <= record["temp_1"] <= TEMP_MAX
    assert TEMP_MIN <= record["temp_2"] <= TEMP_MAX
    assert TEMP_MIN <= record["temp_3"] <= TEMP_MAX
    assert HUM_MIN <= record["humidity"] <= HUM_MAX
    assert SOIL_MIN <= record["soil_humidity"] <= SOIL_MAX
    assert LIGHT_MIN <= record["lighting"] <= LIGHT_MAX

    datetime.fromisoformat(record["date"])


@pytest.mark.parametrize("limit", [1, 3, 5])
def test_get_values(limit):
    response = requests.get(f"{BASE_URL}/sensors/from_db/?limit={limit}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= limit

    if data:
        record = data[0]
        expected_keys = {"id", "uid", "temp_1", "temp_2", "temp_3",
                         "humidity", "soil_humidity", "lighting", "date"}
        assert expected_keys == set(record.keys())
        assert TEMP_MIN <= record["temp_1"] <= TEMP_MAX
        assert TEMP_MIN <= record["temp_2"] <= TEMP_MAX
        assert TEMP_MIN <= record["temp_3"] <= TEMP_MAX
        assert HUM_MIN <= record["humidity"] <= HUM_MAX
        assert SOIL_MIN <= record["soil_humidity"] <= SOIL_MAX
        assert LIGHT_MIN <= record["lighting"] <= LIGHT_MAX
        datetime.fromisoformat(record["date"])
