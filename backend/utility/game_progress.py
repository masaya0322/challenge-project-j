from sqlalchemy.orm import Session
from sqlalchemy import func
from model import GameProgress, RFIDTag, ScannedRFID
from datetime import datetime

def update_game_progress(db: Session):
    """
    現在のゲーム進行状況を計算し、GameProgressテーブルを更新する
    
    Args:
        db: データベースセッション
    """
    # 1. 登録されているおもちゃの総数を取得
    total_toys = db.query(RFIDTag).count()
    
    # 2. 現在片付けが完了している（＝直近でスキャンされた）おもちゃの数を取得
    # ScannedRFIDテーブルには直近のスキャン履歴が残っているため、
    # そこに含まれるユニークなrfid_tagの数をカウントする
    cleaned_toys = db.query(ScannedRFID.rfid_tag).distinct().count()
    
    # GameProgressテーブルのレコードを取得（なければ作成）
    # シングルトンとして扱うため、最初のレコードを取得するか、常にID=1を使う
    game_progress = db.query(GameProgress).first()
    
    if not game_progress:
        game_progress = GameProgress(
            total_toys=total_toys,
            cleaned_toys=cleaned_toys
        )
        db.add(game_progress)
        print(f"GameProgressを作成しました: Total={total_toys}, Cleaned={cleaned_toys}")
    else:
        game_progress.total_toys = total_toys
        game_progress.cleaned_toys = cleaned_toys
        # print(f"GameProgressを更新しました: Total={total_toys}, Cleaned={cleaned_toys}")
    
    db.commit()
    db.refresh(game_progress)
    return game_progress

def get_game_progress(db: Session) -> GameProgress:
    """
    最新のゲーム進行状況を取得する
    
    Args:
        db: データベースセッション
    
    Returns:
        GameProgress: 最新の進行状況レコード
    """
    progress = db.query(GameProgress).first()
    if not progress:
        # レコードがない場合はデフォルト値（すべて0）で作成して返す
        progress = GameProgress()
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return progress
