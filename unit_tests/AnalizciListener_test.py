import os
import unittest   # The test framework
from resources.analizci.AnalizciListener import AnalizciListener


class TestAnalizciListener(unittest.TestCase):
    def test_1_start_suite(self):
        name = "Workspace.Tests.KT_CN_001"
        analizci = AnalizciListener()
        attributes = {}
        analizci.start_suite(name, attributes)
        print("Sonuç >>> ")

    def test_1_end_suite(self):
        # Given
        test_name = os.getenv("TEST_ID")
        suite_name = "Workspace.Tests.KT_CN_001"
        attributes = {}
        # *.pcap dosyası oluşturmak için
        ansible = AnsibleManager()
        ansible.start_packet_capture()
        ansible.fetch_pcap_files(test_name)
        # When
        self.test_1_start_suite()
        analizci = AnalizciListener()
        analizci.end_suite(suite_name, attributes)
        # Then
        print("Sonuç >>> ")


if __name__ == '__main__':
    unittest.main()
