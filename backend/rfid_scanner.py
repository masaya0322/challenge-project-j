import sys
import time
from utility.rfid_connect import establish_connection, SERIAL_PORT
from utility.rfid_command import send_rfid_command
from model import parse_inventory_response
from db_connect import SessionLocal
from utility.database import process_and_save_tags, delete_old_scanned_records

INVENTORY_INTERVAL = 1.0

def send_inventory_command(ser):
    inventory_command = "0200550110036B0D"
    print("--- UHF_Inventory コマンド送信 ---")
    response = send_rfid_command(ser, inventory_command)
    
    if response:
        inventory_response = parse_inventory_response(response)
        return inventory_response

if __name__ == "__main__":
    ser = establish_connection()
    if not ser:
        print("接続の確立に失敗しました。")
        sys.exit(1)

    try:
        print(f"\nInventoryコマンドを{INVENTORY_INTERVAL}秒間隔で実行します。")
        print("検出されたタグは自動的にデータベースに保存されます。")
        print("10秒以上古いスキャンレコードは自動的に削除されます。")
        print("終了するには Ctrl+C を押してください。\n")
        
        loop_count = 1
        while True:
            print(f"\n{'='*60}")
            print(f"実行回数: {loop_count}")
            print(f"{'='*60}")
            
            response = send_inventory_command(ser)
            
            if response and response.is_success():
                response.print_tags()
                
                db = SessionLocal()
                try:
                    print("\n=== データベース保存処理 ===")
                    process_and_save_tags(response, db)
                finally:
                    delete_old_scanned_records(db, seconds=10)
                    db.close()
            else:
                print("\nInventoryコマンドの実行に失敗しました。")
            
            loop_count += 1
            
            time.sleep(INVENTORY_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nユーザーによって中断されました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()
            print(f"\n{SERIAL_PORT} を閉じました。")
