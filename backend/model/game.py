from sqlalchemy import Column, Integer, Float, DateTime, String
from datetime import datetime
from db_connect import Base

class GameProgress(Base):
    """ゲーム進行状況"""
    __tablename__ = "game_progress"
    
    # シングルトン的に使うため、固定IDまたは1つのレコードのみを想定
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    total_toys = Column(Integer, default=0, nullable=False)        # 登録されているおもちゃの数
    cleaned_toys = Column(Integer, default=0, nullable=False)      # 片付けが完了しているおもちゃの数
