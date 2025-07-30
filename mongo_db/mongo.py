from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["dynamic_impact_tool"]

def get_user_collection():
    return db["users"]

def get_file_collection():
    return db["files"]

def get_chat_collection():
    return db["chats"]
def get_mongo_client():
    uri = "mongodb://localhost:27017/"
    return MongoClient(uri)