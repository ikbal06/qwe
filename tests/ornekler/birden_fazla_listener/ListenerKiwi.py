# from resources.common.Logger import log
from robot.libraries.BuiltIn import BuiltIn
logger = BuiltIn()


class ListenerKiwi:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        logger.log_to_console("\nKiwiListener ---> __init__")
        self.ROBOT_LIBRARY_LISTENER = self
        self.top_suite_name = None

    def start_suite(self, name, attributes):
        logger.log_to_console(f"\nKiwiListener ---> start_suite > name:{name}  <> attributes: {attributes}")
        if self.top_suite_name is None:
            self.top_suite_name = name
            logger.log_to_console(f"// ----->  This is the top-level test: {name}")

    def start_test(self, name, attributes):
        logger.log_to_console(f"\nKiwiListener ---> start_test > name:{name}  <> attributes: {attributes}")

    def end_test(self, name, attributes):
        logger.log_to_console(f"\nKiwiListener ---> end_test > name:{name}  <> attributes: {attributes}")

    def end_suite(self, name, attributes):
        logger.log_to_console(f"\nKiwiListener ---> end_suite > name:{name}  <> attributes: {attributes}")
        if name == self.top_suite_name:
            logger.log_to_console(f"  This is the top-level test: {name} // <-----")
