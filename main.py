from flask import Flask, request
import telegram
import os

TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    if text == "/start":
        bot.sendMessage(chat_id=chat_id, text="Welcome to VMP Bot – Cleans spaces, Happy Faces!")
    else:
        bot.sendMessage(chat_id=chat_id, text=f"You said: {text}")

    return "ok"
