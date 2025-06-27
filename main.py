from fastapi import FastAPI

# FastAPIアプリを作成
app = FastAPI()

# ルート（エンドポイント）を定義
@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}