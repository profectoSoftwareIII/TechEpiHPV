from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Servidor ejecutandose"}
