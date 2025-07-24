from pymongo import MongoClient

def test_mongo_connection():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        # List all databases
        dbs = client.list_database_names()
        print("✅ MongoDB connected successfully!")
        print("📚 Available Databases:", dbs)
    except Exception as e:
        print("❌ MongoDB connection failed:", e)

if __name__ == "__main__":
    test_mongo_connection()
