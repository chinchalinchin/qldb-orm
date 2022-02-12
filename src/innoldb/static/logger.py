import logging
from innoldb import settings


def getLogger(name: str) -> logging.Logger:
    """
    Returns an instance of the :class:`logging.Logger` class configured to print events on the `logging.INFO` level to `stdout`. Add special methods for logging application environment and logging dictionaries, via the `log_env` and `log_dict` methods.

    :param name: Name of the module instantiating the :class:`logging.Logger`.
    :type name: str

    :return: Instance of Logger.
    :rtype: :class:`logging.Logger`
    """
    logFormatter = logging.Formatter(
        "%(asctime)s [%(levelname)-5.5s] [{}] %(message)s".format(name))
    logger = logging.getLogger(name)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.setLevel(settings.get_log_level())
    logger.addHandler(consoleHandler)
    return logger
