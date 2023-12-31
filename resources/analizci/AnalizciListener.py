import os
# import json
from pathlib import Path
import subprocess
from datetime import datetime
from urllib.parse import urlparse
from robot.libraries.BuiltIn import BuiltIn
from resources.common.Logger import log
from resources.spirent.SpirentManager import SpirentManager
from resources.globalProperties import *
from resources.analizci.AnalizciClient import AnalizciClient

_sp = SpirentManager()


def get_target_report_directory(_spirent_test_id):
    # Tüm test çıktılarını içerecek klasör
    test_artifact_directory = os.getenv('output_path')
    log.debug(f"Hedef dizin test_artifact_directory: {test_artifact_directory}")
    return os.path.join(test_artifact_directory, _spirent_test_id)


def get_target_pcap_directory(_spirent_test_id):
    # Testin PCAP çıktılarını içerecek klasör
    test_artifact_directory = get_target_report_directory(_spirent_test_id)
    spirent_pcaps_dir_name = 'spirent_pcap_files'
    log.debug(f"Hedef dizin spirent_pcaps_dir_name: {spirent_pcaps_dir_name}")
    return os.path.join(test_artifact_directory, spirent_pcaps_dir_name)


def save_test_result_files():
    # Dosyaları çektiğimiz haliyle, fiziki dosya yollarını içeren dizi olarak döneceğiz
    saved_files = []
    spirent_test_id = BuiltIn().get_variable_value('${SPIRENT_TEST_ID}')
    spirent_running_test_id = BuiltIn().get_variable_value('${SPIRENT_RUNNING_TEST_ID}')
    test_status = _sp.get_test_status(spirent_running_test_id)
    tr_spirent_pcap_path = get_target_pcap_directory(spirent_test_id)
    file_list = test_status.get("resultFilesList")
    if not os.path.exists(tr_spirent_pcap_path):
        log.info(f'PCAP Dosyalarının dizini mevcut değil, yaratılacak tr_spirent_pcap_path: {tr_spirent_pcap_path}')
        Path(tr_spirent_pcap_path).mkdir(parents=True, exist_ok=True, mode=0o755)

    for url in file_list:
        # URL şuna benzer geliyor http://10.10.20.74/results/automated/23-09-29_15.13.59__RID-869__KT_CN_001.log.txt
        # Ancak biz değişken IP adresinden erişmek istiyoruz. Biraz değiştirip şunun gibi bir adrese dönüştüreceğiz:
        # http://192.168.13.77/results/automated/23-09-29_15.13.59__RID-869__KT_CN_001.log.txt
        try:
            if not url.endswith("pcap"):
                continue

            parsed_url = urlparse(url)
            absolute_path = parsed_url.path
            new_url = f'{SPIRENT_PROTOCOL}://{SPIRENT_IP}/{absolute_path}'
            log.debug(f"wget {new_url} -P {tr_spirent_pcap_path}")
            wget_result = subprocess.call(f"wget {new_url} -P {tr_spirent_pcap_path}", shell=True,)
            if wget_result == 0:
                log.info(f'{new_url} Spirent dosyası başarıyla indirildi.')
                file_name = os.path.basename(parsed_url.path)
                saved_files.append(f'{tr_spirent_pcap_path}/{file_name}')
            else:
                log.warning(f'Spirent report={new_url} could not received')

        except Exception as e:
            log.error(f'Spirent report={new_url} not received. Error={e}')
            return None

        return saved_files


class AnalizciListener():

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.top_suite_name = None
        self.testId = None

    def start_suite(self, name, attributes):
        # Bir koşuda birden fazla test suit'in koşması istenirse her suite_start
        # Kiwi üzerinde yeni bir "Test Run" yaratmasın diye ilk "top_suite_name"
        # değişkeni kullanılacak.
        self.testId = name
        if self.top_suite_name is None:
            self.top_suite_name = name

    def end_suite(self, name, attributes):
        # if name == self.top_suite_name:  # içine girince hatayı buradan verdi
        # TODO: Analizci çalışsın
        # robot dosyasının içinde varsa bu şekilde
        # files = save_test_result_files()

        if name == self.testId:  # içine girince hatayı buradan verdi
            selectected_test_id = str(self.testId).replace(" ", "_")

            fullPath = "/tmp/test_outputs/"+selectected_test_id+"/nf_pcap_files/"
            print("/tmp/test_outputs/"+selectected_test_id+"/nf_pcap_files/")
            for gzFile in os.listdir(fullPath):
                if gzFile.endswith(".gz"):
                    subprocess.check_output("gunzip "+fullPath+gzFile, shell=True, text=True)
            pcapList = []
            for pcapFile in os.listdir(fullPath):
                if pcapFile.endswith(".pcap"):
                    pcapList.append(pcapFile.split("_")[1].split(".")[0])

            # Convert strings to datetime objects
            date_objects = [datetime.strptime(date, '%d-%m-%Y-%H-%M-%S') for date in pcapList]
            # Find the latest date
            latest_pcap = max(date_objects)
            # Convert it back to a string
            latest_date_pcap = latest_pcap.strftime('%d-%m-%Y-%H-%M-%S')

            for pcapFile in os.listdir(fullPath):
                if pcapFile.endswith(".pcap"):
                    if latest_date_pcap in pcapFile:
                        print(fullPath+pcapFile)
                        analizci_config_obj = AnalizciClient(
                            "http://analizci-test-back.ulakhaberlesme.com.tr/automated/", pcap_name=fullPath + pcapFile,
                            test_id=selectected_test_id)
                        merged_pcapname = analizci_config_obj.upload_pcap()
                        if merged_pcapname:
                            analizci_config_obj.run_analyze(merged_pcapname)
                        else:
                            print("[NOK] Analizci run test fail!!!!")
                        break

    def close(self):
        pass
