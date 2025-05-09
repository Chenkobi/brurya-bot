import telebot
import os
from flask import Flask
from threading import Thread
from math import ceil

app = Flask('')
@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

buildings = {
    "בניין 1": 48,
    "בניין 2": 60,
    "בניין 3": 64,
    "בניין 4": 64,
    "בניין 5": 51
}
total_apartments = sum(buildings.values())

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "שלום! שלח לי סכום (בש\"ח), ואחשב כמה כל בניין צריך לשלם (בעיגול כלפי מעלה).")

@bot.message_handler(func=lambda message: message.text.replace('.', '', 1).isdigit())
def calculate_share(message):
    try:
        total_cost = float(message.text)
        cost_per_apartment = total_cost / total_apartments
        result_lines = [
            f"הוצאה כוללת: {total_cost:,.2f} ש\"ח",
            f"עלות לדירה (חישוב מדויק): {cost_per_apartment:,.2f} ש\"ח\n"
        ]
        for name, count in buildings.items():
            raw_amount = count * cost_per_apartment
            rounded_amount = ceil(raw_amount)
            result_lines.append(f"{name}: {rounded_amount:,} ש\"ח ({count} דירות)")
        bot.reply_to(message, "\n".join(result_lines))
    except Exception as e:
        bot.reply_to(message, "שגיאה: ודא ששלחת מספר תקין.")
        print(f"שגיאה במהלך חישוב: {e}")

@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.reply_to(message, "אנא שלח סכום במספרים בלבד.")

bot.infinity_polling()
