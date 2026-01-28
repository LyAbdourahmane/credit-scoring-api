import joblib
import json
import os
import pandas as pd

def test_model_prediction():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(BASE_DIR, "models", "model.pkl")
    metadata_path = os.path.join(BASE_DIR, "models", "metadata.json")

    model = joblib.load(model_path)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    cols = metadata["input_columns"]

    sample = pd.DataFrame([{
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
        "NAME_FAMILY_STATUS": "Single",
        "CREDIT_TERM": 10000 / 200000
    }])

    sample = sample[cols]

    proba = model.predict_proba(sample)[0, 1]

    assert 0 <= proba <= 1
