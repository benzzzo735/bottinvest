from telegram import ReplyKeyboardMarkup

PORTFOLIO_MENU = ReplyKeyboardMarkup(
    [
        ["📊 Показать портфель"],
        ["🔄 Обновить"],
        ["⬅️ Назад"],
    ],
    resize_keyboard=True
)
