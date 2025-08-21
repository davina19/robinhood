from pathlib import Path
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired
from .config import settings
from .db import AsyncSessionLocal
from sqlalchemy import select
from .models import User

SESS_DIR = Path(__file__).parent / "storage" / "sessions"
SESS_DIR.mkdir(parents=True, exist_ok=True)

_clients: dict[int, Client] = {}

async def prepare_login(user_id: int, phone: str):
    """
    Kirim code ke nomor (Telegram akan mengirim via app/SMS).
    Simpan client agar bisa sign_in saat user kirim OTP.
    """
    sess_path = SESS_DIR / f"{user_id}.session"
    app = Client(
        name=str(sess_path),
        api_id=settings.TG_API_ID,
        api_hash=settings.TG_API_HASH,
        in_memory=False,
        workdir=str(SESS_DIR)
    )
    await app.connect()
    await app.send_code(phone_number=phone)
    _clients[user_id] = app
    return True, "Kode dikirim"

async def login_or_attach(user_id: int, code: str):
    """
    Gunakan OTP (digits only) untuk sign_in. Ambil nomor dari DB jika perlu.
    """
    app = _clients.get(user_id)
    if app is None:
        # Coba attach jika session sudah ada
        sess_path = SESS_DIR / f"{user_id}.session"
        app = Client(
            name=str(sess_path),
            api_id=settings.TG_API_ID,
            api_hash=settings.TG_API_HASH,
            in_memory=False,
            workdir=str(SESS_DIR)
        )
        try:
            await app.connect()
            me = await app.get_me()
            if me:
                _clients[user_id] = app
                return True, "Sudah terhubung"
        except Exception:
            pass
        # belum punya session aktif → ambil nomor
        async with AsyncSessionLocal() as s:
            res = await s.execute(select(User).where(User.tg_user_id == user_id))
            u = res.scalar_one_or_none()
            phone = u.phone if u and u.phone else settings.OWNER_PHONE
        if not phone:
            return False, "Nomor belum terdaftar. Tekan Registrasi lalu kirim kontak."
        await app.connect()
        await app.send_code(phone_number=phone)
        _clients[user_id] = app

    # sign in pakai code
    try:
        await app.sign_in(phone_code=code)
        return True, "Login sukses"
    except SessionPasswordNeeded:
        return False, "Perlu password 2FA. Nonaktifkan 2FA sementara atau tambahkan dukungan 2FA."
    except (PhoneCodeInvalid, PhoneCodeExpired):
        return False, "Kode OTP salah atau kedaluwarsa. Kirim ulang kontak untuk minta kode baru."
    except Exception as e:
        return False, f"Gagal login: {e}"
