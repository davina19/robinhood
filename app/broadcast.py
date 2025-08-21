import asyncio
from pyrogram import Client
from .config import settings

async def send_to_groups(app: Client, targets: list[str], text: str, file_id: str | None = None):
    sent = 0
    for t in targets:
        try:
            if file_id:
                await app.send_cached_media(t, file_id, caption=text)
            else:
                await app.send_message(t, text)
            sent += 1
            await asyncio.sleep(settings.DELAY_BETWEEN_MSG_SEC)
        except Exception:
            await asyncio.sleep(1)
    return sent

async def run_broadcast(app: Client, batches: list[list[str]], text: str, file_id: str | None = None):
    total = 0
    for i, batch in enumerate(batches, 1):
        c = await send_to_groups(app, batch, text, file_id)
        total += c
        if i < len(batches):
            await asyncio.sleep(settings.DELAY_BETWEEN_SESS_SEC)
    return total
