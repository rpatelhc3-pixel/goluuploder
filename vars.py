import os
from os import environ

# ═══════════════════════════════════════
#        API Configuration
# ═══════════════════════════════════════
API_ID = int(os.environ.get("API_ID", "22447622"))
API_HASH = os.environ.get("API_HASH", "543b62d58d3e723e766ba57a984ab65d")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8296583593:AAFdO5i9cj9noPqmeVZl9kbH4nEWWwmI42w")

CREDIT = os.environ.get("CREDIT", "ITsGOLU")

# ═══════════════════════════════════════
#        MongoDB Configuration
# ═══════════════════════════════════════
DATABASE_NAME = os.environ.get("DATABASE_NAME", "CpprivateApi")
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "mongodb+srv://itsgoluAPI:jrMHSipToKUEnmcp@cpprivateapi.ghhp3oz.mongodb.net/?appName=CpprivateApi"
)
MONGO_URL = DATABASE_URL

# ═══════════════════════════════════════
#        Owner & Admin Configuration
# ═══════════════════════════════════════
OWNER_ID = int(os.environ.get("OWNER_ID", "777756062"))

# Parse ADMINS from env, then auto-add OWNER_ID
ADMINS = [int(x) for x in os.environ.get("ADMINS", "").split() if x.strip().isdigit()]
if OWNER_ID not in ADMINS:
    ADMINS.append(OWNER_ID)  # ✅ FIX: Owner हमेशा admin रहेगा

# ═══════════════════════════════════════
#        Channel Configuration
# ═══════════════════════════════════════
PREMIUM_CHANNEL = os.environ.get("PREMIUM_CHANNEL", "")

# ═══════════════════════════════════════
#        Thumbnail Configuration
# ═══════════════════════════════════════
THUMBNAILS = list(map(str, os.environ.get("THUMBNAILS", "").split()))

# ═══════════════════════════════════════
#        Web Server Configuration
# ═══════════════════════════════════════
WEB_SERVER = os.environ.get("WEB_SERVER", "False").lower() == "true"
WEBHOOK = True
PORT = int(os.environ.get("PORT", 8000))

# ═══════════════════════════════════════
#        Message Formats
# ═══════════════════════════════════════
AUTH_MESSAGES = {
    "subscription_active": """<b>🎉 Subscription Activated!</b>

<blockquote>Your subscription has been activated and will expire on {expiry_date}.
You can now use the bot!</blockquote>\n\nType /start to start uploading""",

    "subscription_expired": """<b>⚠️ Your Subscription Has Ended</b>

<blockquote>Your access to the bot has been revoked as your subscription period has expired.
Please contact the admin to renew your subscription.</blockquote>""",

    "user_added": """<b>✅ User Added Successfully!</b>

<blockquote>👤 Name: {name}
🆔 User ID: {user_id}
📅 Expiry: {expiry_date}</blockquote>""",

    "user_removed": """<b>✅ User Removed Successfully!</b>

<blockquote>User ID {user_id} has been removed from authorized users.</blockquote>""",

    "access_denied": """<b>⚠️ Access Denied!</b>

<blockquote>You are not authorized to use this bot.
Please contact the admin to get access.</blockquote>""",

    "not_admin": "⚠️ You are not authorized to use this command!",

    "invalid_format": """❌ <b>Invalid Format!</b>

<blockquote>Use format: {format}</blockquote>"""
}
