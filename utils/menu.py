from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Портфель", callback_data="portfolio")],
        [
            InlineKeyboardButton("📈 Доходность", callback_data="income"),
            InlineKeyboardButton("♻ Ребаланс", callback_data="rebalance"),
        ],
        [
            InlineKeyboardButton("🔮 Прогноз", callback_data="forecast"),
            InlineKeyboardButton("🧾 Налоги", callback_data="taxes"),
        ],
    ])
