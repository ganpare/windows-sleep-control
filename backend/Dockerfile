FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# エントリポイントスクリプトに実行権限を付与
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# モジュールパスを明示的に指定
ENV PYTHONPATH=/app

# エントリポイントスクリプトを使用
CMD ["/app/entrypoint.sh"]
