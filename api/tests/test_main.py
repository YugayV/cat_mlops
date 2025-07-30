import pytest
from fastapi.testclient import TestClient

from api.app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_predict():
    test_data = {
        "inputs": [
            {
                "DV_R": 318,
                "DA_R": 7798,
                "AV_R": 365,
                "AA_R": 7177,
                "PM_R": 9507
            }
        ]
    }
    
    response = client.post("/predict", json=test_data)
    assert response.status_code == 200
    
    result = response.json()
    assert "predictions" in result
    assert "probabilities" in result
    assert "version" in result