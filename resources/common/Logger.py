"""Copyright (c) 2021 ULAK Communications
This file contains basic logging operation
"""

import logging
from robot.api import logger as robot_logger


class MyLogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        return super(MyLogger, self).__init__(name, level)

    def info(self, msg, *args, **kwargs):
        msg = f'>>---> {msg}'
        return super(MyLogger, self).info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return super(MyLogger, self).warning(msg, *args, **kwargs)


# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter(
    '[%(asctime)s] [%(pathname)s:%(lineno)d] %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

# Create the Handler for logging data to a file
logger_handler = logging.FileHandler(filename='output/ulaktestutility.log')
# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)
logger_handler.setLevel(logging.DEBUG)


log = logging.getLogger(__name__)
# Add the Handler to the Logger
log.addHandler(logger_handler)
log.info('Completed configuring logger()!')
