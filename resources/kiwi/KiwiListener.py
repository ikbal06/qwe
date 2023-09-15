
from robot.libraries.BuiltIn import BuiltIn
from kiwi.KiwiClient import *
import os


class KiwiListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.version_file = None
        self.ROBOT_LIBRARY_LISTENER = self

    def start_suite(self, data, result):
        if "DEFAULT_VERSION_PATH" in os.environ:
            self.version_file = os.environ['DEFAULT_VERSION_PATH']
        print("self.version_file: ", self.version_file)

    def end_test(self, test, result):
        print(test)
        pass
        # get test case or create test case
        # add test case

    def end_suite(self, suite, result):
        pass
        # add tag

    def close(self):
        pass
