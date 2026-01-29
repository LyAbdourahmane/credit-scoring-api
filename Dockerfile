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

# Je revien à la version par defaut car j'ai la version gratuite de render
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


