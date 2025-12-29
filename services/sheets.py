import os
import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1XxujrU5z67K6oUyeGbv50AggXAw90zspSgNdkYq2tbA"
SHEET_NAME = "ПОРТФЕЛЬ"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def to_float(value):
    try:
        if value is None:
            return 0.0
        value = str(value).strip()
        if value == "":
            return 0.0
        value = value.replace("₽", "").replace(" ", "").replace(",", ".")
        return float(value)
    except Exception:
        return 0.0


def get_client():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")

    if not creds_json:
        raise RuntimeError("❌ GOOGLE_CREDENTIALS не задана")

    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

    return gspread.authorize(creds)


def load_dataframe():
    gc = get_client()
    sh = gc.open_by_key(SPREADSHEET_ID)
    sheet = sh.worksheet(SHEET_NAME)
    return pd.DataFrame(sheet.get_all_records())


def get_portfolio_summary():
    df = load_dataframe()

    total_value = 0
    rows = []

    for _, row in df.iterrows():
        ticker = row.get("Тикер", "—")
        qty = to_float(row.get("Количество"))
        price = to_float(row.get("Текущая цена"))

        value = qty * price
        total_value += value

        rows.append((ticker, qty, price, value))

    if total_value == 0:
        return "📊 Портфель пуст"

    lines = ["📊 *Портфель*\n"]

    for ticker, qty, price, value in rows:
        share = value / total_value * 100
        emoji = "🟢" if share >= 20 else "🟡" if share >= 10 else "🔵"

        lines.append(
            f"{emoji} *{ticker}*\n"
            f"  Кол-во: {qty:.2f}\n"
            f"  Цена: {price:,.0f} ₽\n"
            f"  Стоимость: {value:,.0f} ₽ ({share:.1f}%)\n"
        )

    lines.append(f"💰 *Итого:* {total_value:,.0f} ₽")
    return "\n".join(lines)


def get_income():
    df = load_dataframe()

    invested = 0
    current = 0

    for _, row in df.iterrows():
        invested += to_float(row.get("Вложено всего"))
        current += to_float(row.get("Количество")) * to_float(row.get("Текущая цена"))

    profit = current - invested
    pct = (profit / invested * 100) if invested > 0 else 0
    emoji = "📈" if profit >= 0 else "📉"

    return (
        f"{emoji} *Доход*\n\n"
        f"Вложено: {invested:,.0f} ₽\n"
        f"Стоимость: {current:,.0f} ₽\n"
        f"Результат: {profit:,.0f} ₽ ({pct:.2f}%)"
    )


def get_taxes():
    df = load_dataframe()

    invested = 0
    current = 0

    for _, row in df.iterrows():
        invested += to_float(row.get("Вложено всего"))
        current += to_float(row.get("Количество")) * to_float(row.get("Текущая цена"))

    profit = current - invested
    tax = profit * 0.13 if profit > 0 else 0

    return (
        "🧾 *Налоги*\n\n"
        f"Прибыль: {profit:,.0f} ₽\n"
        f"Налог (13%): {tax:,.0f} ₽"
    )


def get_buy_hint():
    df = load_dataframe()

    total = 0
    positions = []

    for _, row in df.iterrows():
        qty = to_float(row.get("Количество"))
        price = to_float(row.get("Текущая цена"))
        ticker = row.get("Тикер", "—")

        value = qty * price
        total += value
        positions.append((ticker, value))

    positions.sort(key=lambda x: x[1])

    if not positions or total == 0:
        return "🛒 Портфель пуст"

    weakest = positions[0][0]

    return (
        "🛒 *Что купить*\n\n"
        f"📉 Самая маленькая доля:\n"
        f"*{weakest}*\n\n"
        "📌 Логика:\n"
        "— выравнивание портфеля\n"
        "— снижение перекоса"
    )
