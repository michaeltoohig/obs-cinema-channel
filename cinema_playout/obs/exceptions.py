from cinema_playout.loggerfactory import LoggerFactory

logger = LoggerFactory.get_logger("obs.exceptions")


class OBSError(Exception):
    def __init__(self, *args, **kwargs):
        if "message" in kwargs:
            logger.error(kwargs["message"])

    def __str__(self):
        return self.__class__.__name__


class OBSConnectionError(OBSError):
    def __init__(self, *args, **kwargs):
        OBSError.__init__(self, *args, **kwargs)


class OBSExitError(OBSError):
    def __init__(self, *args, **kwargs):
        OBSError.__init__(self, *args, **kwargs)
