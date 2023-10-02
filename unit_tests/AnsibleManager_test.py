import os
import unittest   # The test framework
from resources.ansible.AnsibleManager import AnsibleManager


class TestAnsibleManager(unittest.TestCase):
    def test_1_copy_ssh_id_to_servers(self):
        ansible = AnsibleManager()
        sonuc = ansible.copy_ssh_id_to_servers()
        print("Sonuç >>> ", sonuc)

    def test_2_get_installed_packages_and_versions(self):
        print("output_path: ", os.getenv('output_path'))
        ansible = AnsibleManager()
        sonuc = ansible.get_installed_packages_and_versions()
        print("Sonuç >>> ", sonuc)

    def test_3_start_packet_capture(self):
        ansible = AnsibleManager()
        sonuc = ansible.start_packet_capture()
        print("Sonuç >>> ", sonuc)

    def test_4_fetch_pcap_files(self):
        ansible = AnsibleManager()
        ansible.start_packet_capture()
        sonuc = ansible.fetch_pcap_files("KT_CN_001")
        print("Sonuç >>> ", sonuc)


if __name__ == '__main__':
    unittest.main()
