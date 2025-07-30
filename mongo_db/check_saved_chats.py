from mongo_db.mongo_handler import get_user_chats

# Replace with your current username
username = "data_comparison"

history = get_user_chats(username)
if history:
    print(f"Found {len(history)} messages for {username}")
    for msg in history:
        print(msg)
else:
    print("No chat history found.")
