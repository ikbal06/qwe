"""Copyright (c) 2021 ULAK Communications
This file contains basic logging operation
"""

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Create the Handler for logging data to a file
logger_handler = logging.FileHandler(filename='ulaktestutility.log')
logger_handler.setLevel(logging.DEBUG)

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('[%(asctime)s] [%(pathname)s:%(lineno)d] %(levelname)s - %(message)s','%Y-%m-%d %H:%M:%S')

# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)

# Add the Handler to the Logger
log.addHandler(logger_handler)
log.info('Completed configuring logger()!')