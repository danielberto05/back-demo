from fastapi import APIRouter
from pydantic import BaseModel
import os
import json

from google.cloud import pubsub_v1
import google.auth


__, project_id = google.auth.default()

topic_id = os.getenv("PUB_SUB_TOPIC")

clients_path = os.path.join("data", "clients.json")


class Client(BaseModel):
    id: int | None = None
    name: str
    email: str | None = ""

class ClientCreate(BaseModel):
    name: str
    email: str | None = ""


clients_router = APIRouter()

@clients_router.get("")
@clients_router.get("/", include_in_schema=False)
async def list_clients():
    with open(clients_path, 'r') as clients:
        clients = json.loads(clients.read())
        return {"clients": clients}

@clients_router.get("/{id}")
async def get_clients_by_id(id: int):
    with open(clients_path, 'r') as clients:
        clients = json.loads(clients.read())
        return {"clients":  [item for item in clients if item["id"] == id]}

@clients_router.post("")
@clients_router.post("/", include_in_schema=False)
async def create_client(request_client: ClientCreate):
    clients = []
    client = None
    with open(clients_path, "r") as clients_file:
        clients = json.loads(clients_file.read())
        last_client_id = clients[-1].get("id")
        client = Client(id=last_client_id + 1, **request_client.dict())
        clients.append(client.dict())

    with open(clients_path, "w") as clients_file:
        clients_file.write(json.dumps(clients, indent=4))
    
    await publish_message(client)

    return {"clients": client}


async def publish_message(client: Client):
    publisher = pubsub_v1.PublisherClient()

    topic_path = publisher.topic_path(project_id, topic_id)
    
    data_request = {
        "name": client.name,
        "email": client.email,
        "message": "Olá! Seja bem vindo a Demo de serverless, este email foi enviado através do Cloud Run!"
    }
    
    data = json.dumps(data_request, ensure_ascii=False).encode("utf-8")
    
    return publisher.publish(topic_path, data)
