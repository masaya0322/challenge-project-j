from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db_connect import Base

class RFIDTag(Base):
    """RFIDタグ一覧"""
    __tablename__ = "rfid_tags"
    rfid_tag = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    scanned_records = relationship("ScannedRFID", back_populates="rfid_tag_relation")

class ScannedRFID(Base):
    """スキャン履歴"""
    __tablename__ = "currently_scanned_tags"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rfid_tag = Column(String, ForeignKey("rfid_tags.rfid_tag"), nullable=False, index=True)
    scanned_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    rfid_tag_relation = relationship("RFIDTag", back_populates="scanned_records")
