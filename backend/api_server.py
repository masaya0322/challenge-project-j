from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware # 追加
from sqlalchemy.orm import Session
from db_connect import get_db, engine, Base
from model import RFIDTag, ScannedRFID
from utility.game_progress import get_game_progress
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

# --- CORS設定 ここから ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 全てのオリジンを許可
    allow_credentials=True,  # クッキーや認証ヘッダーを許可
    allow_methods=["*"],     # 全てのメソッド（GET, POST, OPTIONS等）を許可
    allow_headers=["*"],     # 全てのヘッダーを許可
)
# --- CORS設定 ここまで ---

Base.metadata.create_all(bind=engine)

class RFIDTagCreate(BaseModel):
    rfid_tag: str
    name: str

class RFIDTagResponse(BaseModel):
    rfid_tag: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ScannedRFIDResponse(BaseModel):
    id: int
    rfid_tag: str
    scanned_at: datetime
    
    class Config:
        from_attributes = True

class GameProgressResponse(BaseModel):
    total_toys: int
    cleaned_toys: int
    
    class Config:
        from_attributes = True

@app.get("/api/hello")
def test_hello():
    return {"message": "Hello World"}

@app.get("/api/db-check")
def check_db(db: Session = Depends(get_db)):
    return {"status": "Database connected successfully"}

@app.get("/api/rfid-tags", response_model=List[RFIDTagResponse])
def get_rfid_tags(db: Session = Depends(get_db)):
    tags = db.query(RFIDTag).all()
    return tags

@app.get("/api/rfid-tags/{rfid_tag}", response_model=RFIDTagResponse)
def get_rfid_tag(rfid_tag: str, db: Session = Depends(get_db)):
    tag = db.query(RFIDTag).filter(RFIDTag.rfid_tag == rfid_tag).first()
    if not tag:
        raise HTTPException(status_code=404, detail="RFIDタグが見つかりません")
    return tag

@app.get("/api/currently-scanned-tags", response_model=List[ScannedRFIDResponse])
def get_currently_scanned_tags(db: Session = Depends(get_db)):
    scanned_tags = db.query(ScannedRFID).all()
    return scanned_tags

@app.get("/api/game/progress", response_model=GameProgressResponse)
def get_progress(db: Session = Depends(get_db)):
    return get_game_progress(db)

def handle_rfid_tag_scanned(rfid_tag_id: str, db: Session, default_name: str = "未登録のおもちゃ"):
    """
    RFIDタグが読み取られた時の処理
    
    Args:
        rfid_tag_id: 読み取られたRFIDタグのID
        db: データベースセッション
        default_name: 新規タグの場合のデフォルト名
    
    Returns:
        dict: 処理結果 {"is_new": bool, "rfid_tag": RFIDTag, "scanned_record": ScannedRFID}
    """
    existing_tag = db.query(RFIDTag).filter(RFIDTag.rfid_tag == rfid_tag_id).first()
    
    is_new = False
    if not existing_tag:
        new_tag = RFIDTag(rfid_tag=rfid_tag_id, name=default_name)
        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)
        existing_tag = new_tag
        is_new = True
        print(f"新しいRFIDタグを登録しました: {rfid_tag_id}")
    else:
        print(f"既存のRFIDタグです: {rfid_tag_id}")

    scanned_record = ScannedRFID(rfid_tag=rfid_tag_id)
    db.add(scanned_record)
    db.commit()
    db.refresh(scanned_record)
    print(f"新しいスキャンレコードとして記録しました: {rfid_tag_id} at {scanned_record.scanned_at}")

    return {
        "is_new": is_new,
        "rfid_tag": existing_tag,
        "scanned_record": scanned_record
    }
