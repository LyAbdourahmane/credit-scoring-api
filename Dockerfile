FROM python:3.12-slim

# Installer libgomp pour LightGBM
RUN apt-get update && apt-get install -y libgomp1 --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Installer uv (tool) puis synchroniser les dépendances du pyproject
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev || true

# S'assurer qu'uvicorn est installé dans l'environnement runtime
# (on installe explicitement pour éviter "No module named uvicorn")
RUN python -m pip install --no-cache-dir "uvicorn[standard]"

COPY . .

EXPOSE 8000

# Utiliser la variable PORT fournie par Render si présente
CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info"]
