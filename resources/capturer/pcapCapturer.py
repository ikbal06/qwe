from common.Logger import log


class tcpdumpListener:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    def start_suite(suite, data, result):
        logger.debug('This is a debug message.')
        # suite.tests.create(name='New test')

    def end_suite(self, suite, result):
        logger.debug('This is a debug message. end_suite')

    def start_test(self, test, result):
        logger.debug('This is a debug message. end_suite')

    def end_test(self, test, result):
        logger.debug('This is a debug message. end_suite')

    def start_tcp_dump():
        log.debug("tcpdump started.")
        pcapFile = ""
