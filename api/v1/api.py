from fastapi import APIRouter

from api.v1.endpoints import clients, products

api_router = APIRouter()

api_router.include_router(clients.clients_router, prefix="/clients", tags=["Clients"])
api_router.include_router(products.products_router, prefix="/products", tags=["Products"])
