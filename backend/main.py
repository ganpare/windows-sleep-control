from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import subprocess
import platform
import psutil
import ctypes
from wakeonlan import send_magic_packet
from dotenv import load_dotenv
import pathlib

# 環境変数の読み込み
# プロジェクトルートの.envファイルを読み込む
root_dir = pathlib.Path(__file__).parent.parent
load_dotenv(root_dir / ".env")

app = FastAPI(title="Windows スリープ/復帰 API")

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Windowsマシンの情報
WINDOWS_PC_MAC = os.getenv("WINDOWS_PC_MAC")
WINDOWS_PC_IP = os.getenv("WINDOWS_PC_IP")

class SleepResponse(BaseModel):
    success: bool
    message: str

@app.get("/")
def read_root():
    return {"message": "Windows スリープ/復帰 API"}

@app.get("/status")
def get_status():
    """Windowsマシンのステータスを取得する"""
    try:
        # ここではシンプルにpingで応答があるかどうかで判断
        # 実際の環境では、より高度な方法でステータスを確認する必要がある
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", WINDOWS_PC_IP]
        
        print(f"Executing command: {' '.join(command)}")  # デバッグ用
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Command output: {result.stdout}")  # デバッグ用
        print(f"Command error: {result.stderr}")   # デバッグ用
        print(f"Return code: {result.returncode}") # デバッグ用
        
        if result.returncode == 0:
            return {"status": "awake", "message": "Windowsマシンは起動中です"}
        else:
            return {"status": "sleep", "message": "Windowsマシンはスリープ中または接続できません"}
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error details: {error_details}")  # デバッグ用
        raise HTTPException(status_code=500, detail=f"ステータス確認中にエラーが発生しました: {str(e)}\n{error_details}")

@app.post("/sleep", response_model=SleepResponse)
def sleep_windows():
    """Windowsマシンをスリープ状態にする"""
    try:
        # このエンドポイントはWindowsマシン上で実行する必要がある
        if platform.system() != "Windows":
            return SleepResponse(
                success=False,
                message="このエンドポイントはWindowsマシン上で実行する必要があります"
            )
        
        # Windowsをスリープ状態にする
        ctypes.windll.PowrProf.SetSuspendState(0, 0, 0)
        
        return SleepResponse(
            success=True,
            message="スリープコマンドを送信しました"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"スリープ処理中にエラーが発生しました: {str(e)}"
        )

@app.post("/wake", response_model=SleepResponse)
def wake_windows():
    """Wake-on-LANでWindowsマシンを起動する"""
    try:
        if not WINDOWS_PC_MAC:
            raise HTTPException(
                status_code=400, 
                detail="WindowsマシンのMACアドレスが設定されていません"
            )
        
        # Wake-on-LANパケットを送信
        send_magic_packet(WINDOWS_PC_MAC)
        
        return SleepResponse(
            success=True,
            message=f"Wake-on-LANパケットを送信しました (MAC: {WINDOWS_PC_MAC})"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"起動処理中にエラーが発生しました: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
