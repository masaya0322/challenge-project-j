from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, engine, Base

app = FastAPI()

# データベーステーブルを作成
Base.metadata.create_all(bind=engine)

@app.get("/api/hello")
def test_hello():
    return {"message": "Hello World"}

@app.get("/api/db-check")
def check_db(db: Session = Depends(get_db)):
    return {"status": "Database connected successfully"}