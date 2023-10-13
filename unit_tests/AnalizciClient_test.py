import unittest
from resources.analizci.AnalizciClient import AnalizciClient


class TestAnalizciClient(unittest.TestCase):
    def analizciye_gonderme_secenegi_testi(self, name):
        name = "KT_CN_001"
        a = AnalizciClient.analizciye_gonderme_secenegi(self, name)
        print(a)


if __name__ == '__main__':
    unittest.main()
