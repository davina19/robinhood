from pydantic import BaseModel
import os

class Settings(BaseModel):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    BOT_NAME: str = os.getenv("BOT_NAME", "Robinhood 🏹")
    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "robinhoodsystem_bot")
    NOTIFY_BOT_TOKEN: str | None = os.getenv("NOTIFY_BOT_TOKEN")
    NOTIFY_CHAT_ID: str | None = os.getenv("NOTIFY_CHAT_ID")
    ADMIN_USER_ID: int = int(os.getenv("ADMIN_USER_ID", "0"))
    TG_API_ID: int = int(os.getenv("TG_API_ID", "0"))
    TG_API_HASH: str = os.getenv("TG_API_HASH", "")
    OWNER_USER_ID: int | None = int(os.getenv("OWNER_USER_ID", "0") or 0) or None
    OWNER_USERNAME: str | None = os.getenv("OWNER_USERNAME")
    OWNER_PHONE: str | None = os.getenv("OWNER_PHONE")
    MAINTENANCE: bool = os.getenv("MAINTENANCE", "false").lower() == "true"
    TZ: str = os.getenv("TZ", "Asia/Jakarta")
    WATERMARK: str = os.getenv("WATERMARK", "")
    DB_URL: str = os.getenv("DB_URL", "sqlite+aiosqlite:///./robinhood.db")
    RATE_MSG_PER_GROUP: int = int(os.getenv("RATE_MSG_PER_GROUP", "1"))
    DELAY_BETWEEN_MSG_SEC: int = int(os.getenv("DELAY_BETWEEN_MSG_SEC", "3"))
    DELAY_BETWEEN_SESS_SEC: int = int(os.getenv("DELAY_BETWEEN_SESS_SEC", "60"))

settings = Settings()
