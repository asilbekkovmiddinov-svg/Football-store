import logging
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# --- TAYYOR SOZLAMALAR ---
API_TOKEN = '8956019896:AAEaJfsOR4d59fEIwAQnrtyL_wOp01lIU6c'
GROUP_ID = -1004482212768
CARD_NUMBER = "9860 3501 0897 5409"
CARD_OWNER = "Xusanova Maqsuda"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    web_app_url = "https://github.io"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("⚽️ Do'konni ochish", web_app=WebAppInfo(url=web_app_url)))
    await message.reply(
        f"👋 Xush kelibsiz, <b>{message.from_user.first_name}</b>!\n\n"
        f"Pastdagi <b>⚽️ Do'konni ochish</b> tugmasini bosib, "
        f"o'yin pullari va donatlarni arzon narxlarda xarid qilishingiz mumkin.", 
        reply_markup=markup, 
        parse_mode="HTML"
    )

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_receive(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        if data.get("action") == "buy":
            item = data.get("item")
            price = data.get("price")
            await message.reply(
                f"🛒 <b>Siz tanladingiz:</b> {item}\n"
                f"💰 <b>To'lov summasi:</b> {price}\n\n"
                f"💳 To'lov qilish uchun karta raqami:\n"
                f"<code>{CARD_NUMBER}</code>\n"
                f"👤 Karta egasi: {CARD_OWNER}\n\n"
                f"⚠️ Pulni o'tkazgandan so'ng, to'lov chekini (skrinshotini) "
                f"<b>mana shu yerga rasm formatida yuboring!</b>",
                parse_mode="HTML"
            )
        elif data.get("action") == "deposit":
            await message.reply(
                f"💳 Balansni to'ldirish uchun karta raqami:\n"
                f"<code>{CARD_NUMBER}</code>\n"
                f"👤 Karta egasi: {CARD_OWNER}\n\n"
                f"Pulni o'tkazgandan so'ng, chekni (skrinshotni) shu yerga rasm formatida yuboring.",
                parse_mode="HTML"
            )
    except Exception as e:
        logging.error(f"Xatolik: {e}")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def forward_screenshot(message: types.Message):
    user = message.from_user
    caption_text = (
        f"🔔 <b>Yangi to'lov cheki keldi!</b>\n\n"
        f"👤 <b>Foydalanuvchi:</b> {user.full_name}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
        f"🔗 <b>Username:</b> @{user.username if user.username else 'yoq'}\n\n"
        f"📌 Bankingizni tekshiring va pul tushgan bo'lsa, donatni yetkazib bering."
    )
    await bot.send_photo(chat_id=GROUP_ID, photo=message.photo[-1].file_id, caption=caption_text, parse_mode="HTML")
    await message.reply("✅ Rahmat! To'lov chekingiz adminga (guruhga) yuborildi. Tez orada tekshirilib, donat yetkaziladi.")

if __name__ == '__main__':
    from aiohttp import web
    async def handle(request): return web.Response(text="Bot is running!")
    app = web.Application()
    app.router.add_get('/', handle)
    
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(skip_updates=True))
    web.run_app(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
  
