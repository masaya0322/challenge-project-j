import sys
from rfid_connect import establish_connection, SERIAL_PORT
from rfid_utility import send_rfid_command
from rfid_tag import parse_inventory_response

def send_inventory_command(ser):
    """UHF_Inventoryコマンドを送信してタグ情報を取得"""
    # UHF_Inventory: 02 00 55 01 10 03 6B 0D
    inventory_command = "0200550110036B0D"
    print("--- UHF_Inventory コマンド送信 ---")
    response = send_rfid_command(ser, inventory_command)
    
    if response:
        # レスポンスを解析
        inventory_response = parse_inventory_response(response)
        return inventory_response

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
