from telegram import ReplyKeyboardMarkup

BUY_MENU = ReplyKeyboardMarkup(
    [
        ["🛒 Подсказка покупки"],
        ["🧠 Анализ портфеля"],
        ["⬅️ В главное меню"],
    ],
    resize_keyboard=True
)
