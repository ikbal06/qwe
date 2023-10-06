import unittest   # The test framework
from resources.kiwi.KiwiClient import KiwiClient


class TestKiwiClient(unittest.TestCase):

    def test_TestRun_create(self):
        """
        Test that it can sum a list of integers
        """
        kc = KiwiClient()
        response = kc.TestRun_create(7)
        self.assertGreater(response['result']['id'], 0)


if __name__ == '__main__':
    unittest.main()
