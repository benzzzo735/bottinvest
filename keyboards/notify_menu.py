from telegram import ReplyKeyboardMarkup

NOTIFY_MENU = ReplyKeyboardMarkup(
    [
        ["🔔 Включить уведомления"],
        ["🔕 Выключить уведомления"],
        ["⬅️ В главное меню"],
    ],
    resize_keyboard=True
)

