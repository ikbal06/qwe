"""Copyright (c) 2021 ULAK Communications
This file contains basic logging operation
"""

import logging
from robot.api import logger as robot_logger


class MyLogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        self.setLevel(logging.DEBUG)
        return super(MyLogger, self).__init__(name, level)

    def info(self, msg, *args, **kwargs):
        msg = f'>>---> {msg}'
        return super(MyLogger, self).info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return super(MyLogger, self).warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            self._custom_debug(msg, args[0])
        else:
            return super(MyLogger, self).debug(msg, *args, **kwargs)

    def _custom_debug(self, message, info_dict):
        # ------------------
        # ----- mesaj ------
        # ------------------
        # Property 1: değer
        # Property 2: değer
        # ------------------
        # Mesajın uzunluğunu hesaplayın ve bu uzunluğa uygun şekilde - karakterlerini oluşturun
        message_length = len(message)
        dashes = '-' * (message_length + 36)  # 36 karakter, diğer eklemeler ve boşluklar için ayrıldı

        log.info(dashes)
        log.info(f"--- {message} ---")
        log.info(dashes)

        for key, value in info_dict.items():
            log.info(f"{key:<15}: {value}")

        log.info(dashes)


# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter(
    '[%(asctime)s] [%(pathname)s:%(lineno)d] %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

# Create the Handler for logging data to a file
logger_handler = logging.FileHandler(filename='output/ulaktestutility.log')
# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)
logger_handler.setLevel(logging.DEBUG)


log = logging.getLogger(__name__+'.MyLogger')
log.setLevel(logging.DEBUG)
# Add the Handler to the Logger
log.addHandler(logger_handler)

log.debug('debug > Completed configuring logger()!')
log.info('info > Completed configuring logger()!')
log.warning('warning > Completed configuring logger()!')
log.error('error > Completed configuring logger()!')
