import logging
import logging.config
from logging.handlers import RotatingFileHandler


def setup_logging(level=logging.DEBUG, log_file="Application.log"):
    logger = logging.getLogger()
    logger.setLevel(level)

    # logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Пишем в файл
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=50 * 1024,  # 5 MB
        backupCount=1,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    # Чтобы в файл не шли INFO & DEBUG
    file_handler.setLevel(logging.WARNING)

    # Пишем в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


setup_logging()