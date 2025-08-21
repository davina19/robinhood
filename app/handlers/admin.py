from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, F
from datetime import datetime, timedelta
import secrets
from sqlalchemy import insert
from ..db import AsyncSessionLocal
from ..models import Token
from ..config import settings

router = Router()

@router.callback_query(F.data == "ad:menu")
async def admin_menu(c: CallbackQuery):
    if c.from_user.id != settings.ADMIN_USER_ID:
        await c.answer("Admin only", show_alert=True)
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔑 Generate Token", callback_data="ad:gentok")],
        [InlineKeyboardButton(text="🧰 Maintenance", callback_data="ad:maint")]
    ])
    await c.message.answer("🛠 Admin Control", reply_markup=kb)
    await c.answer()

@router.callback_query(F.data == "ad:gentok")
async def gen_menu(c: CallbackQuery):
    if c.from_user.id != settings.ADMIN_USER_ID:
        await c.answer("Admin only", show_alert=True); return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="3 Hari", callback_data="ad:gt:3"),
         InlineKeyboardButton(text="7 Hari", callback_data="ad:gt:7"),
         InlineKeyboardButton(text="30 Hari", callback_data="ad:gt:30")]
    ])
    await c.message.answer("Pilih masa berlaku token:", reply_markup=kb)
    await c.answer()

@router.callback_query(F.data.startswith("ad:gt:"))
async def do_gen(c: CallbackQuery):
    if c.from_user.id != settings.ADMIN_USER_ID:
        await c.answer("Admin only", show_alert=True); return
    days = int(c.data.split(":")[2])
    code = secrets.token_urlsafe(96)
    exp = datetime.utcnow() + timedelta(days=days)
    async with AsyncSessionLocal() as s:
        await s.execute(insert(Token).values(code=code, expires_at=exp))
        await s.commit()
    msg = ("✅Berhasil menginstall bot!\n\n"
           "⚠️Terdapat device yang login (JANGAN DILEPAS, ITU BOTNYA!!!).⚠️\n\n"
           "Jika dilepas maka akan muncul notifikasi perintah buat userbot kembali.\n\n"
           "🗝 Gunakan TOKEN ini untuk mengakses userbot ketika akun Anda terlogout/suspend:\n\n"
           f"{code}\n\nJaga keamanan token Anda dan simpan dengan aman !!!")
    await c.message.answer(msg)
    await c.answer()

@router.callback_query(F.data == "ad:maint")
async def toggle_maint(c: CallbackQuery):
    if c.from_user.id != settings.ADMIN_USER_ID:
        await c.answer("Admin only", show_alert=True); return
    await c.message.answer("Maintenance toggle belum diimplementasikan (stub).")
    await c.answer()
