import logging

from cinema_playout import config
from cinema_playout.telegram import send_message


class TelegramHandler(logging.Handler):
    def emit(self, record):
        message = f"cinema-{config.SERVER_ID}: {record.msg}"
        send_message(message)


class LoggerFactory:
    _LOG = None

    @staticmethod
    def __create_logger(log_file, log_level):
        """
        A private method that interacts with the python logging module
        """
        log_format = "%(asctime)s:%(levelname)s:%(message)s"
        LoggerFactory._LOG = logging.getLogger(log_file)
        logging.basicConfig(level=logging.INFO, format=log_format, datefmt="%Y-%m-%d %H:%M:%S")

        if log_level == "INFO":
            LoggerFactory._LOG.setLevel(logging.INFO)
        elif log_level == "ERROR":
            LoggerFactory._LOG.setLevel(logging.ERROR)
        elif log_level == "DEBUG":
            LoggerFactory._LOG.setLevel(logging.DEBUG)

        tg_handler = TelegramHandler(logging.ERROR)
        LoggerFactory._LOG.addHandler(tg_handler)

        return LoggerFactory._LOG

    @staticmethod
    def get_logger(log_file, log_level=None):
        """
        A static method called by other modules to initialize logger in their own module
        """
        if log_level is None:
            log_level = config.LOG_LEVEL
        logger = LoggerFactory.__create_logger(log_file, log_level)

        # return the logger object
        return logger
