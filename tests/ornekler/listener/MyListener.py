import re
from robot.running.context import sys
import os
from robot.libraries.BuiltIn import BuiltIn
logger = BuiltIn()


class MyListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3
    _tr_id = 0

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.top_suite_name = None
        self.end_suite_name = None
        logger.log('-----> __init__')

    def start_suite(self, name, attributes):
        logger.log(f'start_suite -----> {name}')
        self.end_suite_name = name

        if self.top_suite_name is None:
            self.top_suite_name = name
            logger.log_to_console(f"This is the top-level test: {name}")

    def start_test(self, name, attributes):
        # Teste başlandığında yapılacak işlemler burada tanımlanır
        logger.log_to_console(f'start_test -----> {name}')

    def end_test(self, name, attributes):
        logger.log_to_console(f'end_test -----> {name}')

    def end_suite(self, name, attributes):
        if self.end_suite_name == name:
            logger.log_to_console(f'end_suite -----> {name}')

    def close(self):
        logger.log_to_console(f'close ----->')
