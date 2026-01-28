from fastapi.testclient import TestClient
from main import app, API_KEY

client = TestClient(app)

# -------------------------
# Test endpoint racine
# -------------------------
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# -------------------------
# Test prédiction valide
def test_predict_valid():
    payload = {
        "AMT_REQ_CREDIT_BUREAU_YEAR": 1.0,
        "HOUR_APPR_PROCESS_START": 10,
        "AMT_ANNUITY": 10000,
        "AMT_CREDIT": 200000,
        "EXT_SOURCE_3": 0.5,
        "EXT_SOURCE_2": 0.6,
        "CODE_GENDER": "M",
        "FLAG_PHONE": 1,
        "AMT_GOODS_PRICE": 180000,
        "FLAG_OWN_CAR": "Y",
        "NAME_FAMILY_STATUS": "Single"
    }

    response = client.post(
        "/predict",
        json=payload,
        headers={"x-api-key": API_KEY}
    )

    assert response.status_code == 200
    body = response.json()
    assert "prediction" in body
    assert "probability" in body

# -------------------------
# Test API key manquante
def test_predict_missing_api_key():
    payload = {
        "AMT_REQ_CREDIT_BUREAU_YEAR": 1.0,
        "HOUR_APPR_PROCESS_START": 10,
        "AMT_ANNUITY": 10000,
        "AMT_CREDIT": 200000,
        "EXT_SOURCE_3": 0.5,
        "EXT_SOURCE_2": 0.6,
        "CODE_GENDER": "M",
        "FLAG_PHONE": 1,
        "AMT_GOODS_PRICE": 180000,
        "FLAG_OWN_CAR": "Y",
        "NAME_FAMILY_STATUS": "Single"
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 403

# -------------------------
# Test mauvais type
def test_predict_invalid_type():
    payload = {
        "AMT_REQ_CREDIT_BUREAU_YEAR": "abc",  # mauvais type
        "HOUR_APPR_PROCESS_START": 10,
        "AMT_ANNUITY": 10000,
        "AMT_CREDIT": 200000,
        "EXT_SOURCE_3": 0.5,
        "EXT_SOURCE_2": 0.6,
        "CODE_GENDER": "M",
        "FLAG_PHONE": 1,
        "AMT_GOODS_PRICE": 180000,
        "FLAG_OWN_CAR": "Y",
        "NAME_FAMILY_STATUS": "Single"
    }

    response = client.post(
        "/predict",
        json=payload,
        headers={"x-api-key": API_KEY}
    )

    assert response.status_code == 422
