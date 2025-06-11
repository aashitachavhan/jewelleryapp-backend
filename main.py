from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models import Product, Cart, CartItem
from crud import (
    get_products, get_product, add_to_cart, 
    update_cart_item_quantity, remove_from_cart, 
    clear_cart, get_cart, create_product, update_product, delete_product
)
from database import connect_to_mongo
from bson import ObjectId
import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app = FastAPI()

# Configure CORS with more permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Initialize MongoDB connection
connect_to_mongo()

@app.get("/")
async def root():
    return {"message": "Jewellery Shop API is running"}

# Product endpoints
@app.get("/products/")
async def read_products():
    products = get_products()
    return JSONResponse(content=json.loads(json.dumps(products, cls=CustomJSONEncoder)))

@app.get("/products/{product_id}")
async def read_product(product_id: str):
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return JSONResponse(content=json.loads(json.dumps(product, cls=CustomJSONEncoder)))

@app.post("/products/")
async def create_new_product(product: Product):
    result = create_product(product)
    return {"message": "Product created successfully", "product": result}

@app.put("/products/{name}")
async def update_existing_product(name: str, product: Product):
    result = update_product(name, product)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully"}

@app.delete("/products/{name}")
async def delete_existing_product(name: str):
    result = delete_product(name)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Cart endpoints
@app.get("/cart/{user_id}")
async def read_cart(user_id: str):
    cart = get_cart(user_id)
    return JSONResponse(content=json.loads(json.dumps(cart, cls=CustomJSONEncoder)))

@app.post("/cart/{user_id}/add/{product_id}")
async def add_item_to_cart(user_id: str, product_id: str, quantity: int = 1):
    cart = add_to_cart(user_id, product_id, quantity)
    if not cart:
        raise HTTPException(status_code=404, detail="Product not found")
    return JSONResponse(content=json.loads(json.dumps(cart, cls=CustomJSONEncoder)))

@app.put("/cart/{user_id}/update/{product_id}")
async def update_item_quantity(user_id: str, product_id: str, quantity: int):
    cart = update_cart_item_quantity(user_id, product_id, quantity)
    return JSONResponse(content=json.loads(json.dumps(cart, cls=CustomJSONEncoder)))

@app.delete("/cart/{user_id}/remove/{product_id}")
async def remove_item_from_cart(user_id: str, product_id: str):
    cart = remove_from_cart(user_id, product_id)
    return JSONResponse(content=json.loads(json.dumps(cart, cls=CustomJSONEncoder)))

@app.delete("/cart/{user_id}/clear")
async def clear_user_cart(user_id: str):
    cart = clear_cart(user_id)
    return JSONResponse(content=json.loads(json.dumps(cart, cls=CustomJSONEncoder)))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


