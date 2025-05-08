from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hola weon lo lograste"}