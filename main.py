# code de l'api
import json
import os
from dotenv import load_dotenv

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Security, Request
from fastapi.security import APIKeyHeader
from utils.data_validation import CreditInput
#from utils.logging_middleware import LoggingMiddleware


#------------------------------------------------------------------------------
# ---------- Chargement du modèle et des métadonnées (une seule fois) ----------
load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
METADATA_PATH = os.path.join(BASE_DIR, "models", "metadata.json")
API_KEY = os.getenv('API_KEY')
api_key_header = APIKeyHeader(name="x-api-key")

def _verify_api_key(x_api_key: str = Security(api_key_header)):
    """Sécurité pour l'endpoint predict"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement du modèle: {e}")

try:
    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)
    INPUT_COLUMNS = metadata.get("input_columns", [])
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement des métadonnées: {e}")

#--------------------------------------------------------------------------------
# ---------- Application FastAPI ----------

app = FastAPI(
    title="Credit Scoring API",
    description="API pour exposer un modèle de scoring crédit (Abdourahamane).",
    version="1.0.0"
)

#app.add_middleware(LoggingMiddleware)

# on exécute une prédiction fictive au demarage ( pour chargé modèles..)
@app.on_event("startup")
def warmup():
    try:
        dummy = {
            "AMT_REQ_CREDIT_BUREAU_YEAR": 1.0,
            "HOUR_APPR_PROCESS_START": 10,
            "AMT_ANNUITY": 20000.0,
            "AMT_CREDIT": 500000.0,
            "EXT_SOURCE_3": 0.5,
            "EXT_SOURCE_2": 0.5,
            "CODE_GENDER": "M",
            "FLAG_PHONE": 1,
            "AMT_GOODS_PRICE": 300000.0,
            "FLAG_OWN_CAR": "Y",
            "NAME_FAMILY_STATUS": "Married"
        }

        df = pd.DataFrame([dummy])
        df["CREDIT_TERM"] = df["AMT_ANNUITY"] / df["AMT_CREDIT"]

        model.predict_proba(df)

        print("Warm-up terminé : modèle chargé en mémoire.")

    except Exception as e:
        print(f"Warm-up échoué : {e}")



@app.get("/")
def root():
    return {
        "message": "Credit Scoring API is running",
        "author": metadata.get("author"),
        "trained_on": metadata.get("trained_on"),
        "dataset_version": metadata.get("dataset_version"),
    }

@app.post("/predict")
def predict(input_data: CreditInput, _: str = Security(_verify_api_key)):
    try:
        # Convertir l'input en DataFrame
        df = pd.DataFrame([input_data.model_dump()])

        # Feature engineering directement sur le DataFrame
        df["CREDIT_TERM"] = df["AMT_ANNUITY"] / df["AMT_CREDIT"]

        # on gère si on nous avons none par des valeurs par défauts
        df = df.fillna({ "AMT_REQ_CREDIT_BUREAU_YEAR": 0, "EXT_SOURCE_3": 0.5, "EXT_SOURCE_2": 0.5 })

        # Prédiction
        proba = float(model.predict_proba(df)[0, 1])
        pred = int(proba > 0.5)

        # Ajout pour le logging (lu par le middleware)
        #request.state.model_output = {
            #"prediction": pred,
            #"probability": proba
        #}

        return {
            "prediction": pred,
            "probability": proba
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la prédiction : {e}")

