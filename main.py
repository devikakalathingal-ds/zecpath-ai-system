from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Zecpath AI Backend Running Successfully"}