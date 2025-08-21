from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# Reply keyboard untuk kontak
share_contact_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📂Daftar📂", request_contact=True)]],
    resize_keyboard=True, one_time_keyboard=True
)

def main_menu(is_admin: bool):
    rows = [
        [InlineKeyboardButton(text="📲 Registrasi", callback_data="reg:menu")],
        [InlineKeyboardButton(text="📩Autoreply📩", callback_data="ar:menu"),
         InlineKeyboardButton(text="🤖Status🤖", callback_data="st:menu")],
        [InlineKeyboardButton(text="🗃Grup & List🗃", callback_data="gl:menu")],
        [InlineKeyboardButton(text="🪩Template Pesan🪩", callback_data="tp:menu")],
        [InlineKeyboardButton(text="⏳Atur Jeda⏳", callback_data="jd:menu"),
         InlineKeyboardButton(text="♻️Reset♻️", callback_data="rs:confirm")],
    ]
    if is_admin:
        rows.append([InlineKeyboardButton(text="🛠 Admin Control", callback_data="ad:menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
