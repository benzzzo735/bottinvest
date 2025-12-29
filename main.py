import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from keyboards.main_menu import MAIN_MENU
from keyboards.portfolio_menu import PORTFOLIO_MENU
from keyboards.buy_menu import BUY_MENU

from services.sheets import (
    portfolio_bcs,
    portfolio_alfa,
    portfolio_all,
    analyze_portfolio,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Это твой инвестиционный бот.",
        reply_markup=MAIN_MENU,
    )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Главное меню
    if text == "📊 Портфель":
        await update.message.reply_text(
            "Выбери портфель:",
            reply_markup=PORTFOLIO_MENU,
        )
        return

    if text == "🛒 Что купить":
        await update.message.reply_text(
            "Выбери действие:",
            reply_markup=BUY_MENU,
        )
        return

    # Портфели
    if text == "🟦 BCS":
        await update.message.reply_text(
            portfolio_bcs(),
            reply_markup=PORTFOLIO_MENU,
            parse_mode="Markdown",
        )
        return

    if text == "🟥 ALFA":
        await update.message.reply_text(
            portfolio_alfa(),
            reply_markup=PORTFOLIO_MENU,
            parse_mode="Markdown",
        )
        return

    if text == "🟨 ВСЕ ВМЕСТЕ":
        await update.message.reply_text(
            portfolio_all(),
            reply_markup=PORTFOLIO_MENU,
            parse_mode="Markdown",
        )
        return

    # Аналитика
    if text == "🧠 Анализ портфеля":
        await update.message.reply_text(
            analyze_portfolio(),
            reply_markup=BUY_MENU,
            parse_mode="Markdown",
        )
        return

    # Назад
    if text == "⬅️ В главное меню":
        await update.message.reply_text(
            "Главное меню",
            reply_markup=MAIN_MENU,
        )
        return


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("SYSTEM START")
    app.run_polling()


if __name__ == "__main__":
    main()
