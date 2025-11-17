"""
データベース操作のユーティリティ関数
データベースのタイムゾーンはUTCである
"""
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from model import RFIDTag, ScannedRFID
from main import handle_rfid_tag_scanned

def print_database_status(db: Session):
    """現在のデータベース状態を表示する"""
    print("\n" + "=" * 60)
    print("===== 現在のRFIDタグ一覧 =====")
    print("=" * 60)
    all_tags = db.query(RFIDTag).all()
    if all_tags:
        for tag in all_tags:
            print(f"  RFID: {tag.rfid_tag}, 名前: {tag.name}, 登録日時: {tag.created_at}")
    else:
        print("  (登録されているタグはありません)")
    
    print("\n" + "=" * 60)
    print("===== 直近10件のスキャン履歴 =====")
    print("=" * 60)
    recent_scans = db.query(ScannedRFID).order_by(ScannedRFID.scanned_at.desc()).limit(10).all()
    if recent_scans:
        for scan in recent_scans:
            print(f"  ID: {scan.id}, RFID: {scan.rfid_tag}, スキャン日時: {scan.scanned_at}")
    else:
        print("  (スキャン履歴はありません)")
    print("=" * 60 + "\n")

def delete_old_scanned_records(db: Session, seconds: int = 10):
    """
    指定秒数以上古いスキャンレコードを削除する
    
    Args:
        db: データベースセッション
        seconds: 削除する基準となる秒数（デフォルト: 10秒）
    
    Returns:
        int: 削除されたレコード数
    """
    # UTCでタイムゾーン情報なしのdatetimeを取得（PostgreSQLと互換性のため）
    now_utc = datetime.utcnow()
    print(f"現在の時刻(UTC): {now_utc}")
    threshold_time = now_utc - timedelta(seconds=seconds)
    
    # 削除対象のレコードを取得
    old_records = db.query(ScannedRFID).filter(
        ScannedRFID.scanned_at < threshold_time
    ).all()
    
    deleted_count = len(old_records)
    
    if deleted_count > 0:
        # レコードを削除
        db.query(ScannedRFID).filter(
            ScannedRFID.scanned_at < threshold_time
        ).delete()
        db.commit()
        print(f"\n{seconds}秒以上古いレコード {deleted_count} 件を削除しました")
    
    return deleted_count

def process_and_save_tags(inventory_response, db: Session):
    """
    検出されたタグをデータベースに保存
    
    Args:
        inventory_response: Inventoryレスポンスオブジェクト
        db: データベースセッション
    """
    if not inventory_response or not inventory_response.is_success():
        return
    
    tags = inventory_response.get_tags()
    if not tags:
        print("保存するタグがありません")
        return
    
    try:
        for tag in tags:
            # EPCをRFIDタグIDとして使用
            rfid_tag_id = tag.epc
            
            # データベースに登録
            print(f"\n--- 次のタグの処理を開始します: {rfid_tag_id} ---")
            result = handle_rfid_tag_scanned(rfid_tag_id, db)
            
            if result["is_new"]:
                print(f"- 新規タグだったので、rfid_tagとcurrently_scanned_tagsテーブルに登録しました")
            else:
                print(f"- 既存タグだったので、currently_scanned_tagsにのみ登録しました")
        
        print(f"\n合計 {len(tags)} 件のタグを正常に処理しました")
        
        # データベースの現在の状態を表示
        print_database_status(db)
    
    except Exception as e:
        print(f"データベース処理中にエラーが発生しました: {e}")
        db.rollback()
        raise