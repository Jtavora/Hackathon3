from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import uvicorn

app = FastAPI()

class Professor(BaseModel):
    name: str
    email: str
    cpf: str


class Student(BaseModel):
    client_email: str
    product: str
    quantity: int
    status: str

@app.get("/", tags=["Root"])
def return_status():
    """Retorna uma mensagem de boas-vindas."""
    return {"message": "Welcome to the API!"}

@app.get("/atividade", tags=["Atividade"])
def get_atividade(client: Client):
    """Retorna uma atividade."""
    client_data = ClientModel(**client.dict())
    client_controller.create(client_data)
    return {"message": "Client created successfully!"}



uvicorn.run(app, host="localhost", port=8000)