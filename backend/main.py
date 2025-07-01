from fastapi import FastAPI

# FastAPIアプリを作成
app = FastAPI()

# ルート（エンドポイント）を定義
@app.get("/api/hello")
def read_root():
    return {"message": "Hello World"}