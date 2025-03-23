FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# モジュールパスを明示的に指定
ENV PYTHONPATH=/app

# app.pyを使用して実行
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
