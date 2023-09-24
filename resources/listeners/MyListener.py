# MyListener.py

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class MyListener:

    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        pass

    def start_suite(self, name, attributes):
        logger.info('-----> This is a debug message.')
        # Test süitine başlandığında yapılacak işlemler burada tanımlanır
        pass

    def start_test(self, name, attributes):
        logger.info('-----> This is a debug message.')
        # Teste başlandığında yapılacak işlemler burada tanımlanır
        pass

    def end_test(self, name, attributes):
        logger.info('-----> This is a debug message.')
        # Test tamamlandığında yapılacak işlemler burada tanımlanır
        pass

    def end_suite(self, name, attributes):
        logger.info('-----> This is a debug message.')
        # Test süiti tamamlandığında yapılacak işlemler burada tanımlanır
        pass
