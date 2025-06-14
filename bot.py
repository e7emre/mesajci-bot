import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
CHANNELS_FILE = "channels.json"

def load_channels():
    if not os.path.exists(CHANNELS_FILE):
        return []
    with open(CHANNELS_FILE, "r") as f:
        return json.load(f)

def save_channels(channels):
    with open(CHANNELS_FILE, "w") as f:
        json.dump(channels, f)

@dp.message()
async def collect_channel(message: types.Message):
    chans = load_channels()
    if message.chat.id not in chans:
        chans.append(message.chat.id)
        save_channels(chans)

@dp.message(Command("broadcast"))
async def broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("Yetkin yok.")
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.answer("Mesaj metni eksik.")
    msg = parts[1]
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="📢 Kanalıma Katıl", url="https://t.me/e7emre")]
            [types.InlineKeyboardButton(text="📢 Admin'e Ulaş", url="https://t.me/e7emrel")]
            [types.InlineKeyboardButton(text="📢 Tüm Kanallara Katıl", url="https://t.me/addlist/2gKNqDkBDZ05YjY0")]
            [types.InlineKeyboardButton(text="📢 Bana Ait Botlar Ve Daha Fazlası İçin Kanala Katıl", url="https://t.me/emo_xyz")]
        ]
    )
    success, fail = 0,0
    for cid in load_channels():
        try:
            await bot.send_message(cid, msg, reply_markup=keyboard)
            success += 1
        except:
            fail += 1
    await message.answer(f"✅ Gönderildi: {success} • ❌ Hata: {fail}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
