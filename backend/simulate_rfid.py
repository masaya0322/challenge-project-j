#!/usr/bin/env python3
"""
RFIDタグのスキャンをシミュレートするスクリプト

使い方:
1. RFIDタグを登録: python simulate_rfid.py register <tag_id> <name>
2. RFIDタグをスキャン: python simulate_rfid.py scan <tag_id>
3. 全てのタグを表示: python simulate_rfid.py list
4. スキャン履歴をクリア: python simulate_rfid.py clear
5. ゲーム進行状況を表示: python simulate_rfid.py progress
6. 特定のタグを削除: python simulate_rfid.py delete <tag_id>
7. 全てのタグを削除: python simulate_rfid.py delete-all
8. タグ名を変更: python simulate_rfid.py rename <tag_id> <new_name>
"""

import sys
from sqlalchemy.orm import Session
from db_connect import SessionLocal, engine, Base
from model import RFIDTag, ScannedRFID, GameProgress
from utility.game_progress import update_game_progress
from datetime import datetime

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e

def register_tag(tag_id: str, name: str):
    """新しいRFIDタグを登録"""
    db = get_db()
    try:
        existing = db.query(RFIDTag).filter(RFIDTag.rfid_tag == tag_id).first()
        if existing:
            print(f"❌ タグ {tag_id} は既に登録されています: {existing.name}")
            return

        new_tag = RFIDTag(rfid_tag=tag_id, name=name)
        db.add(new_tag)
        db.commit()
        print(f"✅ 新しいタグを登録しました: {tag_id} - {name}")

        update_game_progress(db)
    finally:
        db.close()

def scan_tag(tag_id: str):
    """RFIDタグのスキャンをシミュレート"""
    db = get_db()
    try:
        tag = db.query(RFIDTag).filter(RFIDTag.rfid_tag == tag_id).first()
        if not tag:
            print(f"❌ タグ {tag_id} は登録されていません。先に登録してください。")
            return

        scanned = ScannedRFID(rfid_tag=tag_id)
        db.add(scanned)
        db.commit()
        print(f"✅ タグをスキャンしました: {tag_id} - {tag.name}")

        update_game_progress(db)
        show_progress(db)
    finally:
        db.close()

def list_tags():
    """登録されている全てのタグを表示"""
    db = get_db()
    try:
        tags = db.query(RFIDTag).all()
        if not tags:
            print("登録されているタグはありません")
            return

        print("\n📋 登録されているRFIDタグ:")
        print("-" * 60)
        for tag in tags:
            scanned = db.query(ScannedRFID).filter(ScannedRFID.rfid_tag == tag.rfid_tag).first()
            status = "✅ スキャン済み" if scanned else "⬜ 未スキャン"
            print(f"{status} | {tag.rfid_tag} | {tag.name}")
        print("-" * 60)
    finally:
        db.close()

def clear_scans():
    """スキャン履歴をクリア（ゲームリセット）"""
    db = get_db()
    try:
        count = db.query(ScannedRFID).delete()
        db.commit()
        print(f"✅ {count}件のスキャン履歴をクリアしました")

        update_game_progress(db)
        show_progress(db)
    finally:
        db.close()

def delete_tag(tag_id: str):
    """特定のRFIDタグを削除"""
    db = get_db()
    try:
        tag = db.query(RFIDTag).filter(RFIDTag.rfid_tag == tag_id).first()
        if not tag:
            print(f"❌ タグ {tag_id} は登録されていません")
            return

        # 関連するスキャン履歴も削除
        scanned_count = db.query(ScannedRFID).filter(ScannedRFID.rfid_tag == tag_id).delete()

        # タグを削除
        db.delete(tag)
        db.commit()

        print(f"✅ タグを削除しました: {tag_id} - {tag.name}")
        if scanned_count > 0:
            print(f"   関連するスキャン履歴 {scanned_count}件も削除しました")

        update_game_progress(db)
        show_progress(db)
    finally:
        db.close()

def delete_all_tags():
    """全てのRFIDタグを削除"""
    db = get_db()
    try:
        tag_count = db.query(RFIDTag).count()
        if tag_count == 0:
            print("削除するタグはありません")
            return

        # 全てのスキャン履歴を削除
        scanned_count = db.query(ScannedRFID).delete()

        # 全てのタグを削除
        db.query(RFIDTag).delete()
        db.commit()

        print(f"✅ 全てのタグを削除しました: {tag_count}件")
        if scanned_count > 0:
            print(f"   スキャン履歴 {scanned_count}件も削除しました")

        update_game_progress(db)
        show_progress(db)
    finally:
        db.close()

def rename_tag(tag_id: str, new_name: str):
    """RFIDタグの名前を変更"""
    db = get_db()
    try:
        tag = db.query(RFIDTag).filter(RFIDTag.rfid_tag == tag_id).first()
        if not tag:
            print(f"❌ タグ {tag_id} は登録されていません")
            return

        old_name = tag.name
        tag.name = new_name
        db.commit()

        print(f"✅ タグ名を変更しました:")
        print(f"   ID: {tag_id}")
        print(f"   旧名: {old_name}")
        print(f"   新名: {new_name}")
    finally:
        db.close()

def show_progress(db: Session = None):
    """ゲーム進行状況を表示"""
    should_close = False
    if db is None:
        db = get_db()
        should_close = True

    try:
        progress = db.query(GameProgress).first()
        if not progress:
            print("\n📊 ゲーム進行状況: 初期化されていません")
            return

        total = progress.total_toys
        cleaned = progress.cleaned_toys
        percentage = (cleaned / total * 100) if total > 0 else 0

        print(f"\n📊 ゲーム進行状況:")
        print(f"   おもちゃ総数: {total}")
        print(f"   片付け済み: {cleaned}")
        print(f"   進捗率: {percentage:.1f}%")

        if cleaned >= total and total > 0:
            print("   🎉 ゲーム終了！全てのおもちゃを片付けました！")
    finally:
        if should_close:
            db.close()

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1].lower()

    if command == "register":
        if len(sys.argv) < 4:
            print("使い方: python simulate_rfid.py register <tag_id> <name>")
            return
        tag_id = sys.argv[2]
        name = " ".join(sys.argv[3:])
        register_tag(tag_id, name)

    elif command == "scan":
        if len(sys.argv) < 3:
            print("使い方: python simulate_rfid.py scan <tag_id>")
            return
        tag_id = sys.argv[2]
        scan_tag(tag_id)

    elif command == "list":
        list_tags()
        show_progress()

    elif command == "clear":
        clear_scans()

    elif command == "progress":
        show_progress()

    elif command == "delete":
        if len(sys.argv) < 3:
            print("使い方: python simulate_rfid.py delete <tag_id>")
            return
        tag_id = sys.argv[2]
        delete_tag(tag_id)

    elif command == "delete-all":
        confirm = input("⚠️  全てのタグを削除しますか？ (yes/no): ")
        if confirm.lower() == "yes":
            delete_all_tags()
        else:
            print("キャンセルしました")

    elif command == "rename":
        if len(sys.argv) < 4:
            print("使い方: python simulate_rfid.py rename <tag_id> <new_name>")
            return
        tag_id = sys.argv[2]
        new_name = " ".join(sys.argv[3:])
        rename_tag(tag_id, new_name)

    else:
        print(f"不明なコマンド: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
