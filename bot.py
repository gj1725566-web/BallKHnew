import os
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL", "https://t.me/BallKH368BOT/BallFixtureLife")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Launch App", url=APP_URL)],
        [
            InlineKeyboardButton("⚽ Live Scores", callback_data="live"),
            InlineKeyboardButton("📅 Today's Fixtures", callback_data="fixtures"),
        ],
        [
            InlineKeyboardButton("🔍 Team Lookup", callback_data="team"),
            InlineKeyboardButton("🏆 Standings", callback_data="standings"),
        ],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "👋 *Welcome to BallKH368!*\n\n"
        "⚽ Your football companion.\n\n"
        "• Live scores\n"
        "• Today's fixtures\n"
        "• Team lookups\n"
        "• Standings for top leagues\n\n"
        "Tap *Launch App* to open the full experience, "
        "or pick an option below 👇"
    )

    await update.message.reply_text(
        text, reply_markup=reply_markup, parse_mode="Markdown"
    )


# ---------- Button handler ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "live":
        await query.edit_message_text(
            "⚽ *Live Scores*\n\nFetching live matches...\n\n"
            "👉 Open the app for real-time updates.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🚀 Launch App", url=APP_URL)],
                 [InlineKeyboardButton("⬅️ Back", callback_data="back")]]
            ),
            parse_mode="Markdown",
        )

    elif data == "fixtures":
        await query.edit_message_text(
            "📅 *Today's Fixtures*\n\nNo fixtures loaded yet.\n"
            "👉 Open the app to see today's matches.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🚀 Launch App", url=APP_URL)],
                 [InlineKeyboardButton("⬅️ Back", callback_data="back")]]
            ),
            parse_mode="Markdown",
        )

    elif data == "team":
        await query.edit_message_text(
            "🔍 *Team Lookup*\n\nSend a team name or use the app.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🚀 Launch App", url=APP_URL)],
                 [InlineKeyboardButton("⬅️ Back", callback_data="back")]]
            ),
            parse_mode="Markdown",
        )

    elif data == "standings":
        await query.edit_message_text(
            "🏆 *Standings*\n\nOpen the app to view league tables.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🚀 Launch App", url=APP_URL)],
                 [InlineKeyboardButton("⬅️ Back", callback_data="back")]]
            ),
            parse_mode="Markdown",
        )

    elif data == "help":
        await query.edit_message_text(
            "ℹ️ *Help*\n\n"
            "/start – Show main menu\n"
            "/app – Launch the mini app\n"
            "/help – This message\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Back", callback_data="back")]]
            ),
            parse_mode="Markdown",
        )

    elif data == "back":
        # Rebuild the main menu
        keyboard = [
            [InlineKeyboardButton("🚀 Launch App", url=APP_URL)],
            [
                InlineKeyboardButton("⚽ Live Scores", callback_data="live"),
                InlineKeyboardButton("📅 Today's Fixtures", callback_data="fixtures"),
            ],
            [
                InlineKeyboardButton("🔍 Team Lookup", callback_data="team"),
                InlineKeyboardButton("🏆 Standings", callback_data="standings"),
            ],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
        ]
        await query.edit_message_text(
            "👋 *Welcome to BallKH368!*\n\nPick an option below 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )


# ---------- /app ----------
async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🚀 Launch App", url=APP_URL)]]
    await update.message.reply_text(
        "Tap below to launch the app 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ---------- main ----------
def main():
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN missing. Add it to your .env")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("app", app_command))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
