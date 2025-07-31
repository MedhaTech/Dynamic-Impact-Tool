# mongo_db/mongo.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(os.getenv("MONGO_URI"))

# You can name your DB anything consistent
db = client["dynamic_impact_tool"]

def get_user_collection():
    return db["users"]

def get_file_collection():
    return db["files"]

def get_chat_collection():
    return db["chats"]

def get_upload_collection():
    return db["uploads"]

def get_mongo_client():
    return MongoClient(MONGO_URI)

