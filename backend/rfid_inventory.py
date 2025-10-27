import sys
import time
from rfid_connect import establish_connection, SERIAL_PORT
from rfid_test import send_rfid_command

def send_inventory_command(ser):
    """UHF_Inventoryコマンドを送信"""
    # UHF_Inventory: 02 00 55 01 10 03 6B 0D
    inventory_command = "0200550110036B0D"
    print("--- UHF_Inventory コマンド送信 ---")
    response = send_rfid_command(ser, inventory_command)
    return response

if __name__ == "__main__":
    # 接続確立
    ser = establish_connection()
    if not ser:
        print("接続の確立に失敗しました。")
        sys.exit(1)

    try:
        # Inventoryコマンドを送信
        response = send_inventory_command(ser)
        
        if response:
            print("\nInventoryコマンドが正常に実行されました。")
        else:
            print("\nInventoryコマンドの実行に失敗しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()
            print(f"\n{SERIAL_PORT} を閉じました。")
