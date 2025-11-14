import sys
import time
from rfid_connect_util import establish_connection, SERIAL_PORT
from rfid_command_util import send_rfid_command
from rfid_tag import parse_inventory_response
from database import SessionLocal
from main import handle_rfid_tag_scanned

# --- 設定項目 ---
INVENTORY_INTERVAL = 1.0  # Inventoryコマンド実行間隔（秒）

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

def process_and_save_tags(inventory_response):
    """検出されたタグをデータベースに保存"""
    if not inventory_response or not inventory_response.is_success():
        return
    
    tags = inventory_response.get_tags()
    if not tags:
        print("保存するタグがありません")
        return
    
    # データベースセッションを作成
    db = SessionLocal()
    try:
        for tag in tags:
            # EPCをRFIDタグIDとして使用
            rfid_tag_id = tag.epc
            
            # データベースに登録
            result = handle_rfid_tag_scanned(rfid_tag_id, db)
            
            if result["is_new"]:
                print(f"✓ 新規タグを登録: {rfid_tag_id}")
            else:
                print(f"✓ 既存タグをスキャン記録: {rfid_tag_id}")
        
        print(f"\n合計 {len(tags)} 件のタグを処理しました")
    
    except Exception as e:
        print(f"データベース処理中にエラーが発生しました: {e}")
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    # 接続確立
    ser = establish_connection()
    if not ser:
        print("接続の確立に失敗しました。")
        sys.exit(1)

    try:
        print(f"\nInventoryコマンドを{INVENTORY_INTERVAL}秒間隔で実行します。")
        print("検出されたタグは自動的にデータベースに保存されます。")
        print("終了するには Ctrl+C を押してください。\n")
        
        loop_count = 1
        while True:
            print(f"\n{'='*60}")
            print(f"実行回数: {loop_count}")
            print(f"{'='*60}")
            
            # Inventoryコマンドを送信
            response = send_inventory_command(ser)
            
            if response and response.is_success():
                response.print_tags()
                
                # データベースに保存
                print("\n--- データベース保存処理 ---")
                process_and_save_tags(response)
            else:
                print("\nInventoryコマンドの実行に失敗しました。")
            
            loop_count += 1
            
            # 次の実行まで待機
            time.sleep(INVENTORY_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nユーザーによって中断されました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()
            print(f"\n{SERIAL_PORT} を閉じました。")
