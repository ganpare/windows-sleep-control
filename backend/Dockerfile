FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# エントリポイントスクリプトを先にコピーして処理
COPY entrypoint.sh /app/
# 改行コードを修正し、実行権限を付与
RUN sed -i 's/\r$//' /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# その他のファイルをコピー
COPY . .

EXPOSE 8000

# モジュールパスを明示的に指定
ENV PYTHONPATH=/app

# エントリポイントスクリプトを使用
CMD ["/app/entrypoint.sh"]
