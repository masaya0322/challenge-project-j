from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from model import RFIDTag, ScannedRFID
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

# データベーステーブルを作成
Base.metadata.create_all(bind=engine)

# Pydanticモデル（リクエスト/レスポンス用）
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

@app.get("/api/hello")
def test_hello():
    return {"message": "Hello World"}

@app.get("/api/db-check")
def check_db(db: Session = Depends(get_db)):
    return {"status": "Database connected successfully"}

# RFIDタグ（おもちゃ）を登録
@app.post("/api/rfid-tags", response_model=RFIDTagResponse)
def create_rfid_tag(tag: RFIDTagCreate, db: Session = Depends(get_db)):
    # 既に登録されているか確認
    existing_tag = db.query(RFIDTag).filter(RFIDTag.rfid_tag == tag.rfid_tag).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="このRFIDタグは既に登録されています")
    
    # 新規登録
    db_tag = RFIDTag(rfid_tag=tag.rfid_tag, name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

# RFIDタグ（おもちゃ）一覧を取得
@app.get("/api/rfid-tags", response_model=List[RFIDTagResponse])
def get_rfid_tags(db: Session = Depends(get_db)):
    tags = db.query(RFIDTag).all()
    return tags

# 特定のRFIDタグを取得（rfid_tagで検索）
@app.get("/api/rfid-tags/{rfid_tag}", response_model=RFIDTagResponse)
def get_rfid_tag(rfid_tag: str, db: Session = Depends(get_db)):
    tag = db.query(RFIDTag).filter(RFIDTag.rfid_tag == rfid_tag).first()
    if not tag:
        raise HTTPException(status_code=404, detail="RFIDタグが見つかりません")
    return tag

# RFIDタグを削除（rfid_tagで削除）
@app.delete("/api/rfid-tags/{rfid_tag}")
def delete_rfid_tag(rfid_tag: str, db: Session = Depends(get_db)):
    tag = db.query(RFIDTag).filter(RFIDTag.rfid_tag == rfid_tag).first()
    if not tag:
        raise HTTPException(status_code=404, detail="RFIDタグが見つかりません")
    db.delete(tag)
    db.commit()
    return {"message": "RFIDタグを削除しました"}

# 現在スキャンされているRFIDタグ一覧を取得
@app.get("/api/currently-scanned-tags", response_model=List[ScannedRFIDResponse])
def get_currently_scanned_tags(db: Session = Depends(get_db)):
    scanned_tags = db.query(ScannedRFID).all()
    return scanned_tags