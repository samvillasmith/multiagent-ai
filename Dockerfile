FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . . 

RUN pip install --no-cache-dir -e .

EXPOSE 8501
EXPOSE 9999

CMD ["python", "-m", "app.main"]