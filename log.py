import logging
import sys
from logging.handlers import TimedRotatingFileHandler

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(name)s — %(funcName)s:%(lineno)d — %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler('logs.log', when='midnight')
    file_handler.setFormatter(formatter)
    logger.addHandler((file_handler))

    logger.propagate = False

    return logger

