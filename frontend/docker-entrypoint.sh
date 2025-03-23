#!/bin/sh

# 環境変数からバックエンドURLを取得（デフォルト値を設定）
BACKEND_URL=${BACKEND_URL:-http://backend:8000}

# nginx.confファイルを修正して、バックエンドURLを設定
sed -i "s|http://backend:8000|$BACKEND_URL|g" /etc/nginx/conf.d/default.conf

# Nginxを起動
exec "$@"
