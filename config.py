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
from keyboards.income_menu import INCOME_MENU
from keyboards.tax_menu import TAX_MENU
from keyboards.buy_menu import BUY_MENU
from keyboards.notify_menu import NOTIFY_MENU

from services.sheets import (
    get_portfolio_summary,
    get_income,
    get_taxes,
    get_buy_hint,
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Инвест-бот*\nВыбери раздел:",
        reply_markup=MAIN_MENU,
        parse_mode="Markdown"
    )

# ---------- КНОПКИ ----------
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # --- Главное меню ---
    if text == "📊 Портфель":
        await update.message.reply_text("📊 Портфель", reply_markup=PORTFOLIO_MENU)
        return

    if text == "📈 Доход":
        await update.message.reply_text("📈 Доход", reply_markup=INCOME_MENU)
        return

    if text == "🧾 Налоги":
        await update.message.reply_text("🧾 Налоги", reply_markup=TAX_MENU)
        return

    if text == "🛒 Что купить":
        await update.message.reply_text("🛒 Что купить", reply_markup=BUY_MENU)
        return

    if text == "🔔 Уведомления":
        await update.message.reply_text("🔔 Уведомления", reply_markup=NOTIFY_MENU)
        return

    # --- Подменю ---
    if text == "📊 Показать портфель":
        await update.message.reply_text(get_portfolio_summary(), reply_markup=PORTFOLIO_MENU, parse_mode="Markdown")
        return

    if text == "📈 Показать доход":
        await update.message.reply_text(get_income(), reply_markup=INCOME_MENU, parse_mode="Markdown")
        return

    if text == "🧾 Показать налоги":
        await update.message.reply_text(get_taxes(), reply_markup=TAX_MENU, parse_mode="Markdown")
        return

    if text == "🛒 Подсказка покупки":
        await update.message.reply_text(get_buy_hint(), reply_markup=BUY_MENU, parse_mode="Markdown")
        return

    if text == "🔔 Мой статус":
        await update.message.reply_text(
            "🔔 Уведомления активны\n\n"
            "📌 В будущем:\n"
            "— цели\n"
            "— алерты\n"
            "— автосообщения",
            reply_markup=NOTIFY_MENU
        )
        return

    # --- Назад ---
    if text == "⬅️ Назад":
        await update.message.reply_text("⬅️ Главное меню", reply_markup=MAIN_MENU)
        return

# ---------- ЗАПУСК ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    print("SYSTEM START")
    app.run_polling()

if __name__ == "__main__":
    main()
