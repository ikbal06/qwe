# MyListener.py

# from resources.common.Logger import log
from robot.libraries.BuiltIn import BuiltIn
logger = BuiltIn()


class KiwiListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        logger.log_to_console("\nKiwiListener ---> __init__")

    def start_suite(self, name, attributes):
        logger.log_to_console("\nKiwiListener ---> start_suite")

    def start_test(self, name, attributes):
        logger.log_to_console("\nKiwiListener ---> start_test")

    def end_test(self, name, attributes):
        logger.log_to_console("\nKiwiListener ---> end_test")

    def end_suite(self, name, attributes):
        logger.log_to_console("\nKiwiListener ---> end_suite")
