import logging

logging.basicConfig(
    filename="outputs/execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


def log_menu(option):
    logging.info(option)