import ctypes
import sys
import time
import psutil
import platform

def is_windows():
    """実行環境がWindowsかどうかを確認する"""
    return platform.system() == "Windows"

def sleep_windows():
    """Windowsをスリープ状態にする"""
    if not is_windows():
        print("このスクリプトはWindowsでのみ実行できます")
        return False
    
    try:
        # スリープモードに入る
        # 第1引数: 0=スリープ, 1=休止状態
        # 第2引数: 強制的に実行するかどうか
        # 第3引数: ハイブリッドスリープを無効にするかどうか
        ctypes.windll.PowrProf.SetSuspendState(0, 0, 0)
        return True
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False

def get_system_status():
    """システムのステータスを取得する"""
    if not is_windows():
        return {"status": "unknown", "message": "Windowsでのみ実行できます"}
    
    try:
        # バッテリー情報を取得（ノートPCの場合）
        battery = psutil.sensors_battery()
        
        # CPU使用率を取得
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # メモリ使用率を取得
        memory = psutil.virtual_memory()
        
        return {
            "status": "awake",
            "battery": {
                "percent": battery.percent if battery else None,
                "power_plugged": battery.power_plugged if battery else None
            },
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent
        }
    except Exception as e:
        print(f"ステータス取得中にエラーが発生しました: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python windows_sleep.py [sleep|status]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "sleep":
        if sleep_windows():
            print("スリープコマンドを送信しました")
        else:
            print("スリープコマンドの送信に失敗しました")
    
    elif command == "status":
        status = get_system_status()
        print(status)
    
    else:
        print(f"不明なコマンド: {command}")
        print("使用方法: python windows_sleep.py [sleep|status]")
