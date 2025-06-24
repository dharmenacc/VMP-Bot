import os
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application, ApplicationBuilder, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")

app = FastAPI()
bot = Bot(token=BOT_TOKEN)

# Set up Telegram application (not used directly here but needed for webhook)
application = ApplicationBuilder().token(BOT_TOKEN).build()

@app.post("/webhook")
async def handle_webhook(req: Request):
    json_data = await req.json()
    update = Update.de_json(json_data, bot)

    if update.message:
        chat_id = update.message.chat_id
        text = update.message.text

        if text == "/start":
            await bot.send_message(chat_id=chat_id, text="Welcome to VMP Bot – Cleans spaces, Happy Faces!")
        else:
            await bot.send_message(chat_id=chat_id, text=f"You said: {text}")

    return {"status": "ok"}
