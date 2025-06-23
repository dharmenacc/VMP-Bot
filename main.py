from flask import Flask, request
import telegram
import os
from PIL import Image
import io

TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

def get_image_type(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        return img.format.lower()
    except Exception:
        return None

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id

    if update.message.text:
        text = update.message.text
        if text == "/start":
            bot.sendMessage(chat_id=chat_id, text="Welcome to VMP Bot – Cleans spaces, Happy Faces!")
        else:
            bot.sendMessage(chat_id=chat_id, text=f"You said: {text}")
    elif update.message.photo:
        file = bot.getFile(update.message.photo[-1].file_id)
        image_bytes = file.download_as_bytearray()
        img_type = get_image_type(image_bytes)
        bot.sendMessage(chat_id=chat_id, text=f"Received image with type: {img_type}")
    else:
        bot.sendMessage(chat_id=chat_id, text="Unsupported message type")

    return "ok"
