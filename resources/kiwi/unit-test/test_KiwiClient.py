
import unittest   # The test framework
from kiwi.KiwiClient import KiwiClient


class TestKiwiClient(unittest.TestCase):

    def test_TestRun_create(self):
        """
        Test that it can sum a list of integers
        """
        kc = KiwiClient()
        cem = kc.TestRun_create(7)
        self.assertEqual(cem, 6)


if __name__ == '__main__':
    unittest.main()
