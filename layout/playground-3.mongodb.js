// Select the database you're using
use('streamlit_chat_db');

// View all chat records
db.chats.find().pretty();

// Optional: View uploaded files if your app stores them
db.uploads.find().pretty();
