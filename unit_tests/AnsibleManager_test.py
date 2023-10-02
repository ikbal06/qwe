import os
import unittest   # The test framework
from resources.ansible.AnsibleManager import AnsibleManager


class TestAnsibleManager(unittest.TestCase):
    def test_copy_ssh_id_to_servers(self):
        ansible = AnsibleManager()
        sonuc = ansible.copy_ssh_id_to_servers()
        print("Sonuç >>> ", sonuc)

    def test_get_installed_packages_and_versions(self):
        print("output_path: ", os.getenv('output_path'))
        ansible = AnsibleManager()
        sonuc = ansible.get_installed_packages_and_versions()
        print("Sonuç >>> ", sonuc)


if __name__ == '__main__':
    unittest.main()
