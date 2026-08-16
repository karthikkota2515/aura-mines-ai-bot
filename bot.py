import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ACCESS_KEY = os.environ.get("ACCESS_KEY", "CHANGE_ME")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing")

app = Flask(__name__)


@app.route("/")
def home():
    return "AURA Mines AI Bot is running."


def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🔑 Enter Key", callback_data="key"),
            InlineKeyboardButton("📊 Analysis", callback_data="analysis"),
        ],
        [
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        ],
    ]

    text = (
        "💎 *Welcome to AURA Mines AI*\n\n"
        "📊 Game statistics & risk analysis\n"
        "⚡ Fast game insights\n\n"
        "⚠️ *Important:* Mines outcomes are random. "
        "This bot does not guarantee wins or predict the next mine."
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "key":
        context.user_data["waiting_for_key"] = True
        await query.message.reply_text(
            "🔑 Please enter your access key:"
        )

    elif query.data == "analysis":
        await query.message.reply_text(
            "📊 *Mines Analysis*\n\n"
            "🎯 Each round is independent.\n"
            "📈 Previous rounds cannot reliably predict the next round.\n"
            "⚠️ No strategy can guarantee a win.\n\n"
            "Use this bot for information and risk awareness, "
            "not guaranteed predictions.",
            parse_mode="Markdown",
        )

    elif query.data == "help":
        await query.message.reply_text(
            "ℹ️ *AURA Mines AI Help*\n\n"
            "🔑 Enter Key — verify your access key\n"
            "📊 Analysis — view risk/statistical information\n\n"
            "⚠️ Never share your Telegram token, OTP, UPI PIN "
            "or banking password with anyone.",
            parse_mode="Markdown",
        )


async def message_handler(update:
