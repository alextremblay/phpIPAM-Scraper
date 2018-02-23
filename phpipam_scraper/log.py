import logging
from logging.handlers import TimedRotatingFileHandler
import inspect
from pprint import pformat

initialized = False


class CustomLogger(logging.getLoggerClass()):
    def debug_obj(self, msg, obj, *args, **kwargs):
        if inspect.isclass(obj):
            string = pformat((msg, obj.__dict__))
        else:
            string = pformat((msg, obj))
        self.debug(string, *args, **kwargs)


def getLogger(name):
    global initialized
    if not initialized:
        logging.setLoggerClass(CustomLogger)
        logging.getLogger('').setLevel(logging.DEBUG)
        initialized = True
    return logging.getLogger(name)


def enable_console_logging(level):
    levels = {
        1: logging.CRITICAL,
        2: logging.ERROR,
        3: logging.INFO,
        4: logging.DEBUG
    }
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    console.setLevel(levels[level])
    logging.getLogger('').addHandler(console)


def enable_file_logging(filename):
    file = TimedRotatingFileHandler(filename)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    file.setFormatter(formatter)
    file.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(file)
