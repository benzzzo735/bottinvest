from telegram import ReplyKeyboardMarkup

MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["📊 Портфель", "📈 Доход"],
        ["🧾 Налоги", "🛒 Что купить"],
        ["🔔 Уведомления"],
    ],
    resize_keyboard=True
)
