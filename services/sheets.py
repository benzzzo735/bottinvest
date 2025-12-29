import os
import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1XxujrU5z67K6oUyeGbv50AggXAw90zspSgNdkYq2tbA"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def to_float(value):
    try:
        if value is None:
            return 0.0
        value = str(value).replace("₽", "").replace(" ", "").replace(",", ".")
        return float(value)
    except Exception:
        return 0.0


def get_client():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=SCOPES)
    return gspread.authorize(creds)


def load_sheet(sheet_name):
    gc = get_client()
    sh = gc.open_by_key(SPREADSHEET_ID)
    sheet = sh.worksheet(sheet_name)
    return pd.DataFrame(sheet.get_all_records())


def portfolio_summary(sheet_name: str, title: str):
    df = load_sheet(sheet_name)

    total = 0
    rows = []

    for _, row in df.iterrows():
        ticker = row.get("Тикер", "—")
        qty = to_float(row.get("Количество"))
        price = to_float(row.get("Текущая цена"))
        value = qty * price
        total += value

        rows.append((ticker, qty, price, value))

    if total == 0:
        return f"📊 *{title}*\n\nПортфель пуст"

    lines = [f"📊 *{title}*\n"]

    for t, q, p, v in rows:
        pct = v / total * 100
        lines.append(
            f"*{t}* — {v:,.0f} ₽ ({pct:.1f}%)"
        )

    lines.append(f"\n💰 *Итого:* {total:,.0f} ₽")
    return "\n".join(lines)


def portfolio_bcs():
    return portfolio_summary("BCS", "BCS")


def portfolio_alfa():
    return portfolio_summary("ALFA", "ALFA")


def portfolio_all():
    return portfolio_summary("Вместе", "BCS + ALFA")

