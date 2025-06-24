import os
from fastapi import FastAPI, Request
from telegram import Bot, Update
from PIL import Image
import io

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

app = FastAPI()

def get_image_type(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        return img.format.lower()
    except:
        return None

@app.post("/webhook")
async def handle_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    chat_id = update.message.chat.id if update.message else None

    if update.message:
        if update.message.text:
            text = update.message.text
            if text == "/start":
                await bot.send_message(chat_id, "Welcome to VMP Bot – Cleans spaces, Happy Faces!")
            else:
                await bot.send_message(chat_id, f"You said: {text}")
        elif update.message.photo:
            file = await bot.get_file(update.message.photo[-1].file_id)
            content = await file.download_as_bytearray()
            img_type = get_image_type(content)
            await bot.send_message(chat_id, f"Received image type: {img_type}")
    return {"ok": True}
