import time
import json
import logging
from pathlib import Path
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Dossier de logs compatible Render (écriture autorisée uniquement dans /tmp)
# LOG_DIR = Path("logs") car sur render gratuit n'autorise pas
LOG_DIR = Path("/tmp/logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "api_logs.jsonl"

# Logger JSON
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE)
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()

        # Lire le payload brut
        body_bytes = await request.body()
        try:
            payload = json.loads(body_bytes.decode() or "{}")
        except Exception:
            payload = {}

        # ID unique pour tracer la requête
        request_id = str(uuid4())

        # Conteneur pour la prédiction (rempli dans /predict)
        request.state.model_output = None

        # Appel réel de l’endpoint
        response = await call_next(request)

        # Latence
        duration_ms = round((time.time() - start) * 1000, 2)

        # Log structuré
        log_record = {
            "request_id": request_id,
            "timestamp": time.time(),
            "path": request.url.path,
            "method": request.method,
            "status_code": response.status_code,
            "latency_ms": duration_ms,
            "request_payload": payload,
            "model_output": request.state.model_output,
        }

        logger.info(json.dumps(log_record))
        return response
