from database import products_collection
from models import Product

# Create a new product
def create_product(product: Product):
    return products_collection.insert_one(product.dict())

# Get all products
def get_products():
    return list(products_collection.find({}, {"_id": 0}))

# Update a product by name
def update_product(name: str, product: Product):
    return products_collection.update_one({"name": name}, {"$set": product.dict()})

# Delete a product by name
def delete_product(name: str):
    return products_collection.delete_one({"name": name})
