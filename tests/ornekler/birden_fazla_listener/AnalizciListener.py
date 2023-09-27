
from robot.libraries.BuiltIn import BuiltIn
logger = BuiltIn()


class AnalizciListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        logger.log_to_console("\nAnalizciListener ---> __init__")

    def start_suite(self, name, attributes):
        logger.log_to_console("\nAnalizciListener ---> start_suite")

    def start_test(self, name, attributes):
        logger.log_to_console("\nAnalizciListener ---> start_test")

    def end_test(self, name, attributes):
        logger.log_to_console("\nAnalizciListener ---> end_test")

    def end_suite(self, name, attributes):
        logger.log_to_console("\nAnalizciListener ---> end_suite")
