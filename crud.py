from database import products_collection, carts_collection
from models import Product
from bson import ObjectId

# Helper to convert MongoDB document to a serializable dict
def _convert_mongo_doc(doc):
    if doc:
        doc["id"] = str(doc.pop("_id"))
    return doc

# Create a new product
def create_product(product: Product):
    return products_collection.insert_one(product.dict())

# Get all products
def get_products():
    # Convert each product document before returning
    return [_convert_mongo_doc(doc) for doc in products_collection.find()]

# Get a single product by ID
def get_product(product_id: str):
    # Convert product document before returning
    return _convert_mongo_doc(products_collection.find_one({"_id": ObjectId(product_id)}))

# Update a product by name
def update_product(name: str, product: Product):
    return products_collection.update_one({"name": name}, {"$set": product.dict()})

# Delete a product by name
def delete_product(name: str):
    return products_collection.delete_one({"name": name})

# Cart CRUD operations
def get_cart(user_id: str):
    cart = carts_collection.find_one({"user_id": user_id})
    if not cart:
        # Create new cart if it doesn't exist
        cart = {
            "user_id": user_id,
            "items": [],
            "total_price": 0
        }
        carts_collection.insert_one(cart)
    # Convert cart document before returning
    return _convert_mongo_doc(cart)

def add_to_cart(user_id: str, product_id: str, quantity: int = 1):
    # Get product details (already converted by get_product)
    product = get_product(product_id)
    if not product:
        return None

    # Get current cart (already converted by get_cart)
    cart = get_cart(user_id)
    
    # Convert the cart document to make it mutable for updates
    cart = dict(cart) # Ensure it's a mutable dict for modifications

    # Check if product already in cart
    item_found = False
    for item in cart["items"]:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item_found = True
            break

    if not item_found:
        # Add new item to cart
        cart_item = {
            "product_id": product_id,
            "quantity": quantity,
            "name": product["name"],
            "price": product["price"],
            "image": product["image"]
        }
        cart["items"].append(cart_item)
    
    # Update total price
    cart["total_price"] = sum(item["price"] * item["quantity"] for item in cart["items"])
    
    # Save to database (MongoDB will handle ObjectId for query)
    carts_collection.update_one(
        {"user_id": user_id},
        {"$set": {"items": cart["items"], "total_price": cart["total_price"]}},
        upsert=True
    )
    return cart # Convert before returning

def update_cart_item_quantity(user_id: str, product_id: str, quantity: int):
    cart = get_cart(user_id)
    cart = dict(cart) # Ensure mutable

    # Find and update item quantity
    item_found = False
    for item in cart["items"]:
        if item["product_id"] == product_id:
            item["quantity"] = quantity
            item_found = True
            break
            
    if not item_found:
        return cart # Item not in cart, return current cart
    
    # Remove items with quantity 0
    cart["items"] = [item for item in cart["items"] if item["quantity"] > 0]
    
    # Update total price
    cart["total_price"] = sum(item["price"] * item["quantity"] for item in cart["items"])
    
    carts_collection.update_one(
        {"user_id": user_id},
        {"$set": {"items": cart["items"], "total_price": cart["total_price"]}}
    )
    return cart # Convert before returning

def remove_from_cart(user_id: str, product_id: str):
    cart = get_cart(user_id)
    cart = dict(cart) # Ensure mutable
    
    # Remove item
    initial_item_count = len(cart["items"])
    cart["items"] = [item for item in cart["items"] if item["product_id"] != product_id]
    
    if len(cart["items"]) == initial_item_count: # Item not found
        return cart

    # Update total price
    cart["total_price"] = sum(item["price"] * item["quantity"] for item in cart["items"])
    
    carts_collection.update_one(
        {"user_id": user_id},
        {"$set": {"items": cart["items"], "total_price": cart["total_price"]}}
    )
    return cart # Convert before returning

def clear_cart(user_id: str):
    cart = {
        "user_id": user_id,
        "items": [],
        "total_price": 0
    }
    carts_collection.update_one(
        {"user_id": user_id},
        {"$set": cart},
        upsert=True
    )
    return cart # Convert before returning
