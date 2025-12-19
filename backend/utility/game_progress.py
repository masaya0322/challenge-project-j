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
    tidied_toys = db.query(ScannedRFID.rfid_tag).distinct().count()
    
    # 3. 未完了のおもちゃの数を計算
    # 論理的にマイナスにならないようにmax(0, ...)を使う（基本的にはあり得ないが念のため）
    remaining_toys = max(0, total_toys - tidied_toys)
    
    # 4. 達成率を計算
    progress_rate = 0.0
    if total_toys > 0:
        progress_rate = (tidied_toys / total_toys) * 100.0
        # 小数点第2位などで丸めることも可能だが、一旦そのまま保存するか、必要なら丸める
        # ここでは扱いやすさのため、小数点第1位くらいまでにするなどの考慮もありうるが、
        # floatなのでそのままでもよい。表示側で丸めるのが一般的。
    
    # GameProgressテーブルのレコードを取得（なければ作成）
    # シングルトンとして扱うため、最初のレコードを取得するか、常にID=1を使う
    game_progress = db.query(GameProgress).first()
    
    if not game_progress:
        game_progress = GameProgress(
            total_toys=total_toys,
            tidied_toys=tidied_toys,
            remaining_toys=remaining_toys,
            progress_rate=progress_rate
        )
        db.add(game_progress)
        print(f"GameProgressを作成しました: Total={total_toys}, Tidied={tidied_toys}, Rate={progress_rate:.1f}%")
    else:
        game_progress.total_toys = total_toys
        game_progress.tidied_toys = tidied_toys
        game_progress.remaining_toys = remaining_toys
        game_progress.progress_rate = progress_rate
        game_progress.updated_at = datetime.utcnow()
        # print(f"GameProgressを更新しました: Total={total_toys}, Tidied={tidied_toys}, Rate={progress_rate:.1f}%")
    
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
