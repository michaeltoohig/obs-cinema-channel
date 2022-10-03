import logging

from cinema_playout.config import LOG_LEVEL


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
        return LoggerFactory._LOG

    @staticmethod
    def get_logger(log_file, log_level=None):
        """
        A static method called by other modules to initialize logger in their own module
        """
        if log_level is None:
            log_level = LOG_LEVEL
        logger = LoggerFactory.__create_logger(log_file, log_level)

        # return the logger object
        return logger
