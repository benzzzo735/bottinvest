import requests
from utils.helpers import to_float
from utils.logger import logger

class MoexService:
    @staticmethod
    def price(ticker):
        try:
            url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}.json"
            data = requests.get(url, timeout=10).json()
            return to_float(data["marketdata"]["data"][0][12])
        except Exception as e:
            logger.error(f"MOEX {ticker}: {e}")
            return 0.0
