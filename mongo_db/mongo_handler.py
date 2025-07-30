# mongo_db/mongo_handler.py

from mongo_db.mongo import get_chat_collection, get_file_collection
from datetime import datetime
from mongo_db.mongo import get_mongo_client

def save_chat(username, message, response):
    get_chat_collection().insert_one({
        "username": username,
        "role": "user",
        "content": message,
        "timestamp": datetime.now()
    })
    get_chat_collection().insert_one({
        "username": username,
        "role": "ai",
        "content": response,
        "timestamp": datetime.now()
    })

def load_user_chats(username):
    return list(get_chat_collection().find({"username": username}).sort("timestamp", 1))

def save_uploaded_file(username, filename, metadata=None):
    get_file_collection().insert_one({
        "username": username,
        "filename": filename,
        "metadata": metadata or {},
        "timestamp": datetime.now()
    })

def load_user_files(username):
    return list(get_file_collection().find({"username": username}).sort("timestamp", 1))


def get_user_uploads(email: str):
    client = get_mongo_client()
    db = client["Dynamic_Impact_Tool"]  
    collection = db["uploads"]
    uploads = list(collection.find({"email": email}, {"_id": 0}))
    return uploads


def get_user_chats(email: str):
    client = get_mongo_client()
    db = client["Dynamic_Impact_Tool"]
    collection = db["chats"]
    chats = list(collection.find({"email": email}, {"_id": 0}))
    return chats
