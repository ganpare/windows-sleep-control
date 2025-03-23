# Windows スリープ/復帰制御 Webアプリケーション

このプロジェクトはWindowsのスリープと復帰を制御するWebアプリケーションです。

## 機能

- スリープボタン：Windowsをスリープ状態にします
- スリープ解除ボタン：Wake-on-LANを使用してWindowsを復帰させます
- ステータス表示：Windowsがスリープ状態かどうかを表示します

## 技術スタック

- フロントエンド：React, TypeScript
- バックエンド：Python, FastAPI
- Windows操作：Python (psutil, ctypes)
- サーバー：Linux (Ubuntu想定)

## プロジェクト構造

```
windows-sleep/
├── frontend/          # Reactフロントエンド
├── backend/           # FastAPIバックエンド
└── scripts/           # Windowsスリープ制御スクリプト
```

## セットアップ方法

### 通常の開発環境

#### フロントエンド

```bash
cd frontend
npm install
npm start
```

#### バックエンド

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Docker環境

プロジェクトルートディレクトリに`.env`ファイルを作成し、以下の変数を設定してください：

```
WINDOWS_PC_MAC=XX:XX:XX:XX:XX:XX  # WindowsのMACアドレス
WINDOWS_PC_IP=192.168.X.X         # WindowsのIPアドレス
```

Docker Composeを使用して起動：

```bash
docker-compose up -d
```

これにより以下のサービスが起動します：
- フロントエンド: http://localhost:80
- バックエンド: http://localhost:8000

## 環境変数

`.env`ファイルをプロジェクトルートディレクトリに作成し、以下の変数を設定してください：

```
WINDOWS_PC_MAC=XX:XX:XX:XX:XX:XX  # WindowsのMACアドレス
WINDOWS_PC_IP=192.168.X.X         # WindowsのIPアドレス
```
