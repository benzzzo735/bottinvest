from config import NDFL, IIS_TYPE, IIS_LIMIT

class TaxCalculator:
    @staticmethod
    def after_tax(profit):
        return profit * (1 - NDFL)

    @staticmethod
    def iis_refund(contribution):
        if IIS_TYPE == "A":
            return min(contribution, IIS_LIMIT) * NDFL
        return 0
