import os
import unittest   # The test framework
from resources.ansible.AnsibleManager import AnsibleManager
from resources.analizci.AnalizciListener import AnalizciListener
import json


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
        suite_name = "KT_CN_001"
        attributes = {}
        # *.pcap dosyası oluşturmak için
        # ansible = AnsibleManager()
        # ansible.start_packet_capture()
        # ansible.fetch_pcap_files(test_name)
        # When
        self.test_1_start_suite()
        analizci = AnalizciListener()
        analizci.start_suite(suite_name, attributes)
        analizci.end_suite(suite_name, attributes)
        # Then
        print("Sonuç >>> ")

    def test_1_analizciye_gonderme_secenegi(self):

        # JSON dosyasının yolunu belirtin
        json_dosya_yolu = "/workspace/.vscode/launch.json"

        # JSON dosyasını açın ve içeriği yükleyin
        with open(json_dosya_yolu, 'r') as dosya:
            veri = json.load(dosya)

        # "analizciye_gonderme_durumu" değerini alın
        analizciye_gonderme_durumu = veri["configurations"][4]["env"]["analizciye_gonderme_durumu"]

        # Elde edilen değeri yazdırın
        print("Sonuç analizciye gönderme durumu: >>> ", analizciye_gonderme_durumu)


if __name__ == '__main__':
    unittest.main()
