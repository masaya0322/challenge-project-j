# データベースのモデル・スキーマ
# 時刻はUTCを使用する（タイムゾーン情報なし）

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db_connect import Base

class RFIDTag(Base):
    """すべてのRFIDタグ一覧"""
    __tablename__ = "rfid_tags"
    
    rfid_tag = Column(String, primary_key=True, index=True, comment="RFIDタグに登録されているID")
    name = Column(String, nullable=False, comment="RFIDに対応する名前")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="初めて登録されたタイミング")
    
    # リレーションシップ（読み取り履歴との関連）
    scanned_records = relationship("ScannedRFID", back_populates="rfid_tag_relation")


class ScannedRFID(Base):
    """読み取られているRFIDタグ"""
    __tablename__ = "currently_scanned_tags"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rfid_tag = Column(String, ForeignKey("rfid_tags.rfid_tag"), nullable=False, index=True, comment="すべてのRFIDタグ一覧のRFID_tagに対応")
    scanned_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="スキャンされたタイミング")
    
    # リレーションシップ（RFIDタグ一覧との関連）
    rfid_tag_relation = relationship("RFIDTag", back_populates="scanned_records")