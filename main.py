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

from services.sheets import (
    get_portfolio_summary,
    get_income,
    get_taxes,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не найден в .env")


# --------------------
# /start
# --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Инвестиционный бот*\n\nВыбери раздел:",
        reply_markup=MAIN_MENU,
        parse_mode="Markdown"
    )


# --------------------
# Кнопки
# --------------------
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # ГЛАВНОЕ МЕНЮ
    if text == "📊 Портфель":
        await update.message.reply_text(
            "📊 *Портфель*\nВыбери действие:",
            reply_markup=PORTFOLIO_MENU,
            parse_mode="Markdown"
        )
        return

    if text == "📈 Доход":
        await update.message.reply_text(
            get_income(),
            reply_markup=MAIN_MENU,
            parse_mode="Markdown"
        )
        return

    if text == "🧾 Налоги":
        await update.message.reply_text(
            get_taxes(),
            reply_markup=MAIN_MENU,
            parse_mode="Markdown"
        )
        return

    if text == "🛒 Что купить":
        await update.message.reply_text(
            "🛒 *Что купить*\n\n🔧 В разработке",
            reply_markup=MAIN_MENU,
            parse_mode="Markdown"
        )
        return

    if text == "🔔 Уведомления":
        await update.message.reply_text(
            "🔔 *Уведомления*\n\n🔧 В разработке",
            reply_markup=MAIN_MENU,
            parse_mode="Markdown"
        )
        return

    # МЕНЮ ПОРТФЕЛЯ
    if text == "📊 Показать портфель":
        await update.message.reply_text(
            get_portfolio_summary(),
            reply_markup=PORTFOLIO_MENU,
            parse_mode="Markdown"
        )
        return

    if text == "🔄 Обновить":
        await update.message.reply_text(
            "🔄 Данные обновлены",
            reply_markup=PORTFOLIO_MENU
        )
        return

    if text == "⬅️ Назад":
        await update.message.reply_text(
            "⬅️ Главное меню",
            reply_markup=MAIN_MENU
        )
        return

    await update.message.reply_text(
        "❓ Неизвестная команда",
        reply_markup=MAIN_MENU
    )


# --------------------
# Запуск
# --------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("SYSTEM START")
    app.run_polling()


if __name__ == "__main__":
    main()
