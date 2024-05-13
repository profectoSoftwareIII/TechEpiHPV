from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://delightful-plant-0a1f3470f.3.azurestaticapps.net",
    "https://190.165.114.93",
    "https://backendhospitalizacionencasa.azurewebsites.net",
]


@app.get("/")
def hello_world():
    return {"message": "Servidor ejecutandose"}
