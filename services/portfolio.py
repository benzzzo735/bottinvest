from services.moex import MoexService
from utils.helpers import to_float
from config import CATEGORY_TARGETS
import pandas as pd
from services.sheets import load_table

def show_portfolio():
    df = load_table()

    df["Сумма"] = df["Кол-во"] * df["Цена"]
    total = df["Сумма"].sum()

    text = "📊 Портфель\n\n"
    for _, row in df.iterrows():
        text += f"{row['Тикер']}: {row['Сумма']:.0f} ₽\n"

    text += f"\nИтого: {total:.0f} ₽"
    return text

def show_income():
    df = load_table()
    return f"📈 Доходность: {df['Прибыль'].sum():.0f} ₽"


class Portfolio:
    def __init__(self, df):
        self.df = df
        self.total_value = 0

    def update_prices(self):
        prices, values, profits = [], [], []

        for _, row in self.df.iterrows():
            qty = to_float(row["Количество"])
            buy = to_float(row["Цена покупки"])
            price = MoexService.price(row["Тикер"])

            value = qty * price
            profit = (price / buy - 1) * 100 if buy else 0

            prices.append(price)
            values.append(value)
            profits.append(profit)

        self.df["Текущая цена"] = prices
        self.df["Стоимость"] = values
        self.df["Прибыль %"] = profits
        self.total_value = sum(values)

    def recommendation(self):
        result = []
        grouped = self.df.groupby("Категория")["Стоимость"].sum()

        for cat, target in CATEGORY_TARGETS.items():
            cur = grouped.get(cat, 0) / self.total_value
            if cur < target:
                ticker = self.df[self.df["Категория"] == cat].iloc[0]["Тикер"]
                result.append((cat, ticker))
        return result
