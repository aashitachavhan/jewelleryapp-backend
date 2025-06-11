from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    name: str
    category: str
    price: float
    image: str
    description: str = ""

class CartItem(BaseModel):
    product_id: str
    quantity: int
    name: str
    price: float
    image: str

class Cart(BaseModel):
    user_id: str
    items: List[CartItem]
    total_price: float
