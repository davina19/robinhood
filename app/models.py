from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, Boolean, Integer, DateTime, Text
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    is_registered: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[str] = mapped_column(String(16), default="user")  # 'admin'|'user'
    total_broadcast: Mapped[int] = mapped_column(Integer, default=0)

class Token(Base):
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    claimed_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)  # tg_user_id

class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    session_path: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class GroupTarget(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id_or_username: Mapped[str] = mapped_column(String(128))  # -100.. or @username
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    topic_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    list_name: Mapped[str] = mapped_column(String(64), default="default")

class Template(Base):
    __tablename__ = "templates"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    media_file_id: Mapped[str | None] = mapped_column(String(256), nullable=True)
    is_hyperlink: Mapped[bool] = mapped_column(Boolean, default=False)

class AutoFilter(Base):
    __tablename__ = "autofilters"
    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column(String(64), index=True)
    response_text: Mapped[str] = mapped_column(Text)

class Stat(Base):
    __tablename__ = "stats"
    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    uptime_sec: Mapped[int] = mapped_column(Integer, default=0)
    bot_status: Mapped[str] = mapped_column(String(16), default="online")  # online|maintenance
