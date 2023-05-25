from fastapi import APIRouter
from pydantic import BaseModel
import os
import json


products_path = os.path.join("data", "products.json")


class Product(BaseModel):
    id: int
    name: str
    price: float

class ProductCreate(BaseModel):
    name: str
    price: float


products_router = APIRouter()

@products_router.get("")
@products_router.get("/", include_in_schema=False)
async def list_products():
    with open(products_path, 'r') as products:
        products = json.loads(products.read())
        return {"products": products}

@products_router.get("/{id}")
async def get_products_by_id(id: int):
    with open(products_path, 'r') as products:
        products = json.loads(products.read())
        return {"products":  [item for item in products if item["id"] == id]}

@products_router.post("")
@products_router.post("/", include_in_schema=False)
async def create_product(request_product: ProductCreate):
    products = []
    product = None
    with open(products_path, 'r') as products_file:
        products = json.loads(products_file.read())
        last_product_id = products[-1].get("id")
        product = Product(id=last_product_id + 1, **request_product.dict())
        products.append(product.dict())

    with open(products_path, 'w') as products_file:
        products_file.write(json.dumps(products, indent=4))

    return {"products": product}
