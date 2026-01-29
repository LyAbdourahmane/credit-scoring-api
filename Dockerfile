FROM python:3.12-slim

# Installer libgomp pour LightGBM
RUN apt-get update && apt-get install -y libgomp1

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Installer l'outil 'uv' puis installer les dépendances du pyproject
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv \
 && uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

# Démarrer via python -m uvicorn pour être sûr d'utiliser le bon interpréteur
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
