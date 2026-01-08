from flask import redirect, url_for, session
from utils.oauth_client import google
from config.db import user_db
from config.settings import Settings

# -------------------------------------------
# 🌿 Google Login Flow
# -------------------------------------------

def google_login():
    """Redirects the user to Google OAuth for login."""
    redirect_uri = url_for('auth_bp.callback', _external=True)
    return google.authorize_redirect(redirect_uri)


def google_callback():
    """Handles Google's OAuth callback, fetches user info, and stores it."""
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token, nonce=None)
    
    # Store user info in session
    session['user'] = user_info

    # Save user info into MongoDB (avoid duplicates)
    save_user(user_info)

    return user_info


# -------------------------------------------
# 🌿 Save user data to MongoDB
# -------------------------------------------

def save_user(user_info):
    """
    Save user info into MongoDB 'user_db.users' collection.
    If user already exists (same email), skip insertion.
    """
    users_collection = user_db["users"]

    # Check if the user already exists
    existing_user = users_collection.find_one({"email": user_info.get("email")})

    if existing_user:
        print(f"ℹ️ User already exists: {user_info.get('email')}")
    else:
        users_collection.insert_one({
            "name": user_info.get("name"),
            "email": user_info.get("email"),
            "picture": user_info.get("picture"),
            "given_name": user_info.get("given_name"),
            "family_name": user_info.get("family_name"),
        })
        print(f"✅ User saved successfully: {user_info.get('email')}")
