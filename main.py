from fastapi import FastAPI
from models import Product
from crud import create_product, get_products, update_product, delete_product
from fastapi.middleware.cors import CORSMiddleware
from database import connect_to_mongo


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only. Use specific origins in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db():
    connect_to_mongo()


@app.post("/products/")
def add_product(product: Product):
    create_product(product)
    return {"message": "Product added"}

@app.get("/products/")
def list_products():
    return get_products()

@app.put("/products/{name}")
def edit_product(name: str, product: Product):
    update_product(name, product)
    return {"message": "Product updated"}

@app.delete("/products/{name}")
def remove_product(name: str):
    delete_product(name)
    return {"message": "Product deleted"}


