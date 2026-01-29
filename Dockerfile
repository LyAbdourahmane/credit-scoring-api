FROM python:3.12-slim

# Installer libgomp pour LightGBM
RUN apt-get update && apt-get install -y libgomp1

# Installer uv
RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

# j'ai augmenté le nombre de worker ( pour gérer plusieur requêtes en parallèle et reduire la latence)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

