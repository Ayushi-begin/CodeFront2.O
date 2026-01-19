#config/db.py

from pymongo import MongoClient
from config.settings import Settings
from urllib.parse import quote_plus

import os
from dotenv import load_dotenv

load_dotenv()

# If your password has special characters, encode it
username = quote_plus(Settings.MONGO_USER)
password = quote_plus(Settings.MONGO_PASS)

# Build the URI manually
mongo_uri = f"mongodb+srv://{username}:{password}@greeny.4mttjcp.mongodb.net/"

client = MongoClient(mongo_uri)

user_db = client["user_db"]
image_db = client["image_db"]
report_db = client["report_db"]
history_db = client["history_db"]

print("✅ Connected to MongoDB:")
print(f"   - User DB: {user_db.name}")
print(f"   - Image DB: {image_db.name}")
print(f"   - Report DB: {report_db.name}")
print(f"   - History DB: {history_db.name}")
