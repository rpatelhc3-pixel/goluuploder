import os
import time
import certifi
import colorama
from colorama import Fore, Style
from datetime import datetime, timedelta
from typing import Optional, List
from pymongo import MongoClient, errors
from pymongo.database import Database as MongoDatabase
from pymongo.collection import Collection
from vars import MONGO_URL, OWNER_ID, ADMINS

colorama.init()

class Database:
    def init(self, max_retries: int = 3, retry_delay: float = 2.0):  # ✅ FIX: init → init
        self._print_startup_message()
        self.client: Optional[MongoClient] = None
        self.db: Optional[MongoDatabase] = None
        self.users: Optional[Collection] = None
        self.settings: Optional[Collection] = None
        self._connect_with_retry(max_retries, retry_delay)

    def _connect_with_retry(self, max_retries: int, retry_delay: float):
        for attempt in range(1, max_retries + 1):
            try:
                print(f"{Fore.YELLOW}⌛️ Attempt {attempt}/{max_retries}: Connecting to MongoDB...{Style.RESET_ALL}")
                self.client = MongoClient(
                    MONGO_URL,
                    serverSelectionTimeoutMS=20000,
                    connectTimeoutMS=20000,
                    socketTimeoutMS=30000,
                    tlsCAFile=certifi.where(),
                    retryWrites=True,
                    retryReads=True
                )
                self.client.server_info()
                self.db = self.client.get_database('ITsGOLU_db')
                self.users = self.db['users']
                self.settings = self.db['user_settings']
                print(f"{Fore.GREEN}✓ MongoDB Connected Successfully!{Style.RESET_ALL}")
                self._initialize_database()
                return
            except errors.ServerSelectionTimeoutError as e:
                print(f"{Fore.RED}✕ Attempt {attempt} failed: {str(e)}{Style.RESET_ALL}")
                if attempt < max_retries:
                    time.sleep(retry_delay)
                else:
                    raise ConnectionError(f"Failed after {max_retries} attempts") from e
            except Exception as e:
                print(f"{Fore.RED}✕ Unexpected error: {str(e)}{Style.RESET_ALL}")
                raise

    def _print_startup_message(self):
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"🚀 ITsGOLU_UPLOADER Bot - Database Initialization")
        print(f"{'='*50}{Style.RESET_ALL}\n")

    def _initialize_database(self):
        print(f"{Fore.YELLOW}⌛️ Setting up database...{Style.RESET_ALL}")
        try:
            self._create_indexes()
            print(f"{Fore.GREEN}✓ Indexes created!{Style.RESET_ALL}")
            self._migrate_existing_users()
            print(f"{Fore.GREEN}✓ Database ready!{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.RED}⚠️ Init error: {str(e)}{Style.RESET_ALL}")
            raise

    def _create_indexes(self):  # ✅ FIX: class के अंदर लाया
        try:
            self.users.create_index(
                [("bot_username", 1), ("user_id", 1)],
                unique=True, name="user_identity"
            )
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ users index: {str(e)}{Style.RESET_ALL}")
        try:
            self.settings.create_index(
                [("user_id", 1)], unique=True, name="user_settings"
            )
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ settings index: {str(e)}{Style.RESET_ALL}")
        try:
            self.users.create_index(
                "expiry_date", name="user_expiry", expireAfterSeconds=0
            )
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ expiry index: {str(e)}{Style.RESET_ALL}")

    def _migrate_existing_users(self):
        try:
            result = self.users.update_many(
                {"bot_username": {"$exists": False}},
                {"$set": {"bot_username": "ITsGOLU_UPLOADER"}}
            )
            if result.modified_count > 0:
                print(f"{Fore.YELLOW}⚠️ Migrated {result.modified_count} users{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}⚠️ Migration error: {str(e)}{Style.RESET_ALL}")

    def get_user(self, user_id: int, bot_username: str = "ITsGOLU_UPLOADER") -> Optional[dict]:
        try:
            return self.users.find_one({"user_id": user_id, "bot_username": bot_username})
        except Exception as e:
            print(f"{Fore.RED}Error getting user {user_id}: {str(e)}{Style.RESET_ALL}")
            return None

    def is_user_authorized(self, user_id: int, bot_username: str = "ITsGOLU_UPLOADER") -> bool:
        try:
            if user_id == OWNER_ID or user_id in ADMINS:
                return True
            user = self.get_user(user_id, bot_username)
            if not user:
                return False
            expiry = user.get('expiry_date')
            if not expiry:
                return False
            if isinstance(expiry, str):
                expiry = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
            return expiry > datetime.now()
        except Exception as e:
            print(f"{Fore.RED}Auth error {user_id}: {str(e)}{Style.RESET_ALL}")
            return False

    def add_user(self, user_id: int, name: str, days: int,  # ✅ FIX: class के अंदर लाया
                 bot_username: str = "ITsGOLU_UPLOADER") -> tuple:
        try:
            expiry_date = datetime.now() + timedelta(days=days)
            result = self.users.update_one(
                {"user_id": user_id, "bot_username": bot_username},
                {"$set": {
                    "name": name,
                    "expiry_date": expiry_date,
                    "added_date": datetime.now(),
                    "last_updated": datetime.now()
                }},
                upsert=True
            )
            if result.upserted_id or result.modified_count > 0:
                return True, expiry_date
            return False, None
        except Exception as e:
            print(f"{Fore.RED}Add user error {user_id}: {str(e)}{Style.RESET_ALL}")
            return False, None

    def remove_user(self, user_id: int, bot_username: str = "ITsGOLU_UPLOADER") -> bool:
        try:
            result = self.users.delete_one({"user_id": user_id, "bot_username": bot_username})
            return result.deleted_count > 0
        except Exception as e:
            print(f"{Fore.RED}Remove error {user_id}: {str(e)}{Style.RESET_ALL}")
            return False

    def list_users(self, bot_username: str = "ITsGOLU_UPLOADER") -> List[dict]:
        try:
            return list(self.users.find(
                {"bot_username": bot_username},
                {"_id": 0, "name": 1, "user_id": 1, "expiry_date": 1}
            ))
        except Exception as e:
            print(f"{Fore.RED}List users error: {str(e)}{Style.RESET_ALL}")
            return []

    def is_admin(self, user_id: int) -> bool:
        try:
            result = user_id == OWNER_ID or user_id in ADMINS
            if result:
                print(f"{Fore.GREEN}✓ Admin {user_id} verified{Style.RESET_ALL}")
            return result
        except Exception as e:
            print(f"{Fore.RED}Admin check error: {str(e)}{Style.RESET_ALL}")
            return False

    def get_log_channel(self, bot_username: str):
        try:
            settings = self.db.bot_settings.find_one({"bot_username": bot_username})
            if settings and 'log_channel' in settings:
                return settings['log_channel']
            return None
        except Exception as e:
            print(f"Error getting log channel: {str(e)}")
            return None

    def set_log_channel(self, bot_username: str, channel_id: int):  # ✅ FIX: class के अंदर लाया
        try:
            self.db.bot_settings.update_one(
                {"bot_username": bot_username},
                {"$set": {"log_channel": channel_id}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error setting log channel: {str(e)}")
            return False

    def is_channel_authorized(self, channel_id: int, bot_username: str) -> bool:
        try:
            result = self.db.authorized_channels.find_one({
                "channel_id": channel_id,
                "bot_username": bot_username
            })
            return result is not None
        except Exception as e:
            print(f"Channel auth error: {str(e)}")
            return False

    def list_bot_usernames(self) -> List[str]:
        try:
            usernames = self.users.distinct("bot_username")
            return usernames if usernames else ["ITsGOLU_UPLOADER"]
        except Exception as e:
            print(f"{Fore.RED}List bots error: {str(e)}{Style.RESET_ALL}")
            return ["ITsGOLU_UPLOADER"]

    async def cleanup_expired_users(self, bot) -> int:
        try:
            current_time = datetime.now()
            expired_users = self.users.find({
                "expiry_date": {"$lt": current_time},
                "user_id": {"$nin": [OWNER_ID] + ADMINS}
            })
            removed_count = 0
            for user in expired_users:
                try:
                    await bot.send_message(
                        user["user_id"],
                        f"⚠️ Your subscription has expired!\n\n"
                        f"• Name: {user['name']}\n"
                        f"• Expired: {user['expiry_date'].strftime('%d-%m-%Y')}\n\n"
                        f"Contact admin to renew."
                    )
                    self.users.delete_one({"_id": user["_id"]})
                    removed_count += 1
                    log_msg = (
                        f"🚫 Removed Expired User\n\n"
                        f"• Name: {user['name']}\n"
                        f"• ID: {user['user_id']}\n"
                        f"• Expired: {user['expiry_date'].strftime('%d-%m-%Y')}"
                    )
                    for admin in ADMINS + [OWNER_ID]:
                        try:
                            await bot.send_message(admin, log_msg)
                        except:
                            continue
                except Exception as e:
                    print(f"{Fore.YELLOW}Error processing {user['user_id']}: {str(e)}{Style.RESET_ALL}")
                    continue
            return removed_count
        except Exception as e:
            print(f"{Fore.RED}Cleanup error: {str(e)}{Style.RESET_ALL}")
            return 0

    def get_user_expiry_info(self, user_id: int, bot_username: str = "ITsGOLU_UPLOADER") -> Optional[dict]:
        try:
            user = self.get_user(user_id, bot_username)
            if not user:
                return None
            expiry = user.get('expiry_date')
            if not expiry:
                return None
            if isinstance(expiry, str):
                expiry = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
            days_left = (expiry - datetime.now()).days
            return {  # ✅ FIX: सही indent पर लाया
                "name": user.get('name', 'Unknown'),
                "user_id": user_id,
                "expiry_date": expiry.strftime("%d-%m-%Y"),
                "days_left": days_left,
                "added_date": user.get('added_date', 'Unknown'),
                "is_active": days_left > 0
            }
        except Exception as e:
            print(f"{Fore.RED}Expiry info error {user_id}: {str(e)}{Style.RESET_ALL}")
            return None

    def close(self):
        if self.client:
            self.client.close()
            print(f"{Fore.YELLOW}✓ MongoDB closed{Style.RESET_ALL}")

    def enter(self):  # ✅ FIX: enter → enter
        return self

    def exit(self, exc_type, exc_val, exc_tb):  # ✅ FIX: exit → exit
        self.close()


# ═══════════════════════════════════════
#        Initialize DB
# ═══════════════════════════════════════
print(f"\n{Fore.CYAN}{'='*50}")
print(f"🤖 Initializing ITsGOLU_UPLOADER Bot Database")
print(f"{'='*50}{Style.RESET_ALL}\n")

try:
    db = Database(max_retries=3, retry_delay=2)
except Exception as e:
    print(f"{Fore.RED}✕ Fatal: DB init failed! {str(e)}{Style.RESET_ALL}")
    raise
