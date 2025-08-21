import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, Contact
from aiogram.filters import CommandStart
from aiogram import F

from sqlalchemy import select

from .config import settings
from .db import init_db, AsyncSessionLocal
from . import models
from .keyboards import main_menu, share_contact_kb
from .utils import now_id, fmt_full_ts
from .userbot_manager import prepare_login, login_or_attach
from .handlers import admin as admin_handlers

bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()
dp.include_router(router)
dp.include_router(admin_handlers.router)

@dp.message(CommandStart())
async def start(m: Message):
    async with AsyncSessionLocal() as s:
        res = await s.execute(select(models.User).where(models.User.tg_user_id == m.from_user.id))
        u = res.scalar_one_or_none()

    ts = fmt_full_ts(now_id(settings.TZ))
    nickname = m.from_user.first_name or m.from_user.username or str(m.from_user.id)
    total_bc = u.total_broadcast if u else 0
    status_akun = "Terdaftar!" if u and u.is_registered else "Belum terdaftar! (Hubungi Admin untuk registrasi!)"
    uptime = "00:00:00"
    bot_status = "Online ✅" if not settings.MAINTENANCE else "Maintenance ❎"

    text = (
        f"✧ 𝐇𝐞𝐥𝐥𝐨 {nickname}! ✧\n\n"
        f"🗓 {ts}\n⁀➴\n"
        "<code>👤 User Details :\n"
        f"└ ID : {m.from_user.id}\n"
        f"└ Username : @{m.from_user.username or '-'}\n"
        f"└ Status Akun : {status_akun}\n"
        f"└ Total Broadcast : {total_bc}\n\n"
        "📈 BOT Statistics :\n"
        f"└ Bot Status : {bot_status}\n"
        f"└ Total Running : {uptime}</code>\n\n"
        "✧-=[Created by 𝖗𝖔𝖇𝖎𝖓𝖍𝖔𝖔𝖉]=-✧"
    )
    is_admin = (m.from_user.id == settings.ADMIN_USER_ID)
    await m.answer(text, reply_markup=main_menu(is_admin))

@dp.callback_query(F.data == "reg:menu")
async def reg_menu(c: CallbackQuery):
    await c.message.answer(
        "Tekan tombol daftar dibawah untuk mendaftarkan akun anda ke bot!",
        reply_markup=share_contact_kb
    )
    await c.answer()

@dp.message(F.contact)
async def got_contact(m: Message):
    contact: Contact = m.contact
    # simpan nomor; status belum login userbot hingga OTP sukses
    async with AsyncSessionLocal() as s:
        res = await s.execute(select(models.User).where(models.User.tg_user_id == m.from_user.id))
        u = res.scalar_one_or_none()
        if not u:
            u = models.User(tg_user_id=m.from_user.id, username=m.from_user.username, phone=contact.phone_number, is_registered=False)
            s.add(u)
        else:
            u.phone = contact.phone_number
        await s.commit()
    # kirim kode OTP via Pyrogram
    ok, msg = await prepare_login(m.from_user.id, contact.phone_number)
    if ok:
        await m.answer(
            "Silakan Periksa Kode OTP dari Akun Telegram Resmi. Kirim Kode OTP dengan memisahkan setiap kode dengan SPASI.\n"
            "Contoh :\nKode OTP yang diterima : 12345\nKirim dengan spasi : 1 2 3 4 5"
        )
    else:
        await m.answer(f"Gagal meminta kode: {msg}")

@dp.message(F.text.regexp(r"^(?:\d\s+){3,}\d$"))
async def otp_handler(m: Message):
    code = m.text.replace(" ", "")
    ok, msg = await login_or_attach(user_id=m.from_user.id, code=code)
    if ok:
        # tandai terdaftar
        async with AsyncSessionLocal() as s:
            res = await s.execute(select(models.User).where(models.User.tg_user_id == m.from_user.id))
            u = res.scalar_one_or_none()
            if u:
                u.is_registered = True
                await s.commit()
        await m.answer("✅ Login berhasil!")
    else:
        await m.answer(f"❌ {msg}")

# Placeholder untuk menu lain agar tidak 'diam' saat ditekan
@dp.callback_query(F.data.in_({"ar:menu","st:menu","gl:menu","tp:menu","jd:menu","rs:confirm"}))
async def placeholders(c: CallbackQuery):
    text = {
        "ar:menu": "💬 AutoPM — menu akan diisi (stub).",
        "st:menu": "🤖 Status — menu akan diisi (stub).",
        "gl:menu": "🗃 Grup & List — menu akan diisi (stub).",
        "tp:menu": "🪩 Template Pesan — menu akan diisi (stub).",
        "jd:menu": "⏳ Atur Jeda — menu akan diisi (stub).",
        "rs:confirm": "♻️ Reset — konfirmasi & aksi akan diisi (stub).",
    }[c.data]
    await c.message.answer(text)
    await c.answer()

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
