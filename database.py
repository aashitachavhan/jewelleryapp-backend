# from pymongo import MongoClient
# import os

# MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
# client = MongoClient(MONGO_URL)

# from pymongo import MongoClient
# from pymongo.server_api import ServerApi

# import os
# from dotenv import load_dotenv

# load_dotenv()

# # MongoDB URI from environment variable
# uri = os.getenv('MONGODB_URI')



# # Global MongoDB client
# client = None

# def connect_to_mongo():
#     global client
#     client = MongoClient(uri, server_api=ServerApi('1'))
#     try:
#         # Test the connection
#         client.admin.command('ping')
#         print("Pinged your deployment. You successfully connected to MongoDB!")
#         db = client["jewelleryDB"]
#         products_collection = db["products"]
#     except ConnectionError as e:
    
#         print(f"Could not connect to MongoDB: {e}")

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB URI from environment variable
uri = os.getenv('MONGODB_URI')

# Global MongoDB client and collections
client = None
db = None
products_collection = None
carts_collection = None

def connect_to_mongo():
    global client, db, products_collection, carts_collection
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        # Test the connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        # Connect to the database and collections
        db = client["jewelleryDB"]
        products_collection = db["products"]
        carts_collection = db["carts"]

    except PyMongoError as e:
        print(f"Could not connect to MongoDB: {e}")

connect_to_mongo()
        
