import logging

logging.basicConfig(
    filename="invest.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("INVEST")
