from fastapi import FastAPI

app = FastAPI()

@app.get("/api/hello")
def test_hello():
    return {"message": "Hello World"}