# MyListener.py

from robot.api import logger


class MyListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        logger.info('-----> This is a debug message.')
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
