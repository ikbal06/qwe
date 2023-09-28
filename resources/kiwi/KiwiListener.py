"""Kiwi üstünde Test Planına ait bir Test Koşusu (Test Run) yaratılacak (1).
    Test Koşusunda kullanılan NF'lerin adları ve sürümleri etiket (Tag) olarak koşuya eklenecek (2).
    Spirent Test Sonuçlarında Test Planının içindeki Test Senaryoları (Test Case) varsa,
    bu test senaryosu için Test Execution yaratılarak (3) testin sonucu Test Execution içinde güncellenecek (4).
"""
from os.path import exists
import sys
from robot.libraries.BuiltIn import BuiltIn
from kiwi.KiwiClient import *
import os
from common.Logger import log
from spirent.SpirentManager import SpirentManager
import re

# ------------------------------

_kc = KiwiClient()
_sm = SpirentManager()
_kiwi_run_id = 0


def get_test_results(spirent_running_test_id):
    # test_results = _sm.get_test_results_mngr(test_run_id_in=running_test_id)
    test_results = _sm.get_test_results_json(spirent_running_test_id)
    all_test_status = test_results['criteriaStatus']  # 'PASSED'

    test_results_for_kiwi = []
    for r in test_results['criteria']:
        # [ PASS if (Ng Setup Request) (Ng Setup Request) ] metninden "Ng Setup Request"
        # değerini çıkaracak
        extract_step_desc = re.search(r'\((.*?)\)', r['description'])
        if extract_step_desc:
            desc = re.search(r'\((.*?)\)', r['description']).group(1)
        test_step_status = r['status']
        test_results_for_kiwi.append(f"[{test_step_status}] {desc}")

    return {
        "spirent_running_test_id": spirent_running_test_id,  # spirentta o an koşan testin nosu
        "spirent_test_summary": '\n'.join(test_results_for_kiwi),
        "spirent_test_status": all_test_status
    }


def create_test_run_on_kiwi():
    # 1
    kiwi_plan_id = os.environ.get('KIWI_PLAN_ID')
    tr = _kc.TestRun_create(kiwi_plan_id).get('result', {})
    log.debug(f'Test koşusu yaratıldı: {tr}')

    tr_id = tr.get('id')
    if tr_id is None:
        log.error('Test koşu numarası None olamaz!')
        raise Exception('Test koşu numarası None olamaz!')

    log.debug(f'Test koşusu {tr_id} ID değeriyle oluşturuldu')
    return tr_id


def add_versions_as_tags(version_file, tr_id):

    if not version_file:
        msg = 'Test için kullanılan NF paketlerinin sürüm bilgilerini içeren dosya değeri boş olamaz!'
        log.warning(msg)
        raise Exception(msg)

    if not exists(version_file):
        log.warning(f'NF sürümlerini içeren "{version_file}" dosya bulunamadı!')
        return None

    # Dosyayı açıp satırları bir liste içine alıyoruz
    with open(version_file) as f:
        tags = f.read().splitlines()

    tag_responses = []
    for t in tags:
        tag_responses.append(_kc.TestRun_add_tag(tr_id, t))

    return tag_responses


def add_test_case_into_run(kiwi_plan_id, kiwi_run_id, spirent_test_id, spirent_test_result):
    """"Spirent test sonucunun TEST_ID değeriyle Test Plan içindeki Test Senaryolarının SUMMARY değeri aynı ise
    Test Plan için yaratılan Test Koşusuna eklenen Test Case'in ilişkili olduğu Test Execution güncellenir.
    Test Senaryosunun durumu (GEÇTİ/KALDI) ve Spirent içinde bu senaryoyla ilişkili Test Steps bilgileri Comment olarak eklenir.
    """

    cases = _kc.get_TestCase_by_plan_id(kiwi_plan_id).get('result', [])
    found_cases = [tc for tc in cases if tc['summary'] == spirent_test_id]
    if len(found_cases) == 0:
        log.warning(f"{spirent_test_id} ID'li Spirent Test, {kiwi_plan_id}'li Kiwi Test Planıyla ilişkili senaryolarda yok!")
        return None

    if len(found_cases) > 0:
        tc = found_cases[0]
        tc_id = tc['id']
        te = _kc.TestRun_add_case(kiwi_run_id, tc_id).get('result', [])

        if len(te) == 0:
            log.error(f"Test Execution could not created")
            sys.exit(109)

        te = te[0]
        log.debug(f"> Brand new Test Execution created for {tc_id} ")

        te_id = te["id"]
        # Test koşusuna eklediğimiz Test Senaryolarının durumlarını giriyoruz

        status_id = 4 if spirent_test_result["spirent_test_status"] == 'PASSED' else 5

        a = _kc.TestExecution_update(te_id, kiwi_run_id, tc_id, status_id)
        log.debug(f"Test Execution updated {a}")
        comment = spirent_test_result["spirent_test_summary"]
        add_comment = _kc.TestExecution_add_comment(te_id, comment)
        return add_comment


def push_test_results_to_kiwi(kiwi_plan_id, kiwi_run_id, spirent_test_id, spirent_test_result):
    """Test sonuçlarını Kiwi'ye basar."""
    # Test planındaki Test Senaryolarını -> Test koşusuna ekliyoruz
    add_test_case_into_run(kiwi_plan_id, kiwi_run_id, spirent_test_id, spirent_test_result)


def push_test_results_to_kiwi_master(spirent_test_result):
    """"Kiwi üstünde Test Planına ait bir Test Koşusu (Test Run) yaratılacak (1).
    Test Koşusunda kullanılan NF'lerin adları ve sürümleri etiket (Tag) olarak koşuya eklenecek (2).
    Spirent Test Sonuçlarında Test Planının içindeki Test Senaryoları (Test Case) varsa,
    bu test senaryosu için Test Execution yaratılarak (3) testin sonucu Test Execution içinde güncellenecek (4).
    """
    # Test planı için bir test koşusu yaratıyoruz
    # plan_id = 1  # kiwi-testten bak bi ona göre düznele. bir de sışarıdan alacak şekilde olmlaı ya da en azından robot dosyasından
    kc = KiwiClient()
    # 1
    kiwi_plan_id = spirent_test_result['kiwi_plan_id']
    tr = _kc.testrun_create(kiwi_plan_id).get('result', {})
    tr_id = tr.get('id')
    if tr_id is None:
        log.error('Test koşu numarası None olamaz!')
        raise Exception('Test koşu numarası None olamaz!')

    # 2
    # Test koşusuna ortamdaki NF'leri sürümleriyle birlikte etiket olarak giriyoruz
    file_path = 'version.txt'
    # TODO: Eğer dosya yoksa hata fırlat
    tags = _kc.get_tags(file_path) or []
    for t in tags:
        _kc.testrun_add_tag(tr_id, t)

    # run için illa oradaki testleri mi koşmalıyız. eğer verilen test id yoksa oluşturulmalı(test case)
    # test planına eklenmeli ona göre yeni koşu oluşturmalıyız
    # ya da verilen plana göre içindeki test caselere bakılacak o test case varsa sadece o koşulaack
    # Test planındaki Test Senaryolarını -> Test koşusuna ekliyoruz
    # 3
    spirent_test_id = BuiltIn().get_variable_value('${SPIRENT_TEST_ID}')
    tc_names = []
    cases = _kc.get_TestCase_by_plan_id(kiwi_plan_id).get('result', [])
    found_cases = [tc for tc in cases if tc['summary'] == spirent_test_id]
    if len(found_cases) > 0:
        tc = found_cases[0]
        tc_id = tc['id']
        te = _kc.TestRun_add_case(tr_id, tc_id).get('result', [])

        if len(te) == 0:
            log.error(f"Test Execution could not created")
            sys.exit(999)

        te = te[0]
        log.debug(f"> Brand new Test Execution created for {tc_id}: ", te)

        te_id = te["id"]
        # Test koşusuna eklediğimiz Test Senaryolarının durumlarını giriyoruz

        status_id = 4 if spirent_test_result["spirent_test_status"] == 'PASSED' else 5

        a = _kc.TestExecution_update(te_id, tr_id, tc_id, status_id)
        log.debug("Test Execution updated", a)
        comment = spirent_test_result["spirent_test_summary"]
        os.environ['COMMENT'] = comment
        add_comment = _kc.TestExecution_add_comment(te_id, comment)
        return add_comment


def send_test_result_to_kiwi(kiwi_plan_id, kiwi_run_id,  spirent_test_id, spirent_running_test_id):
    """"KIWI_PLAN_ID Test Planı için Test Koşusu yaratıldı.
    Test Planındaki Test Case'ler (KT_CN_01, KT_CN_21 .. gibi) için Test Execution'lar oluşturuldu.
    Spirent testlerinden SPIRENT_TEST_ID için (KT_CN_01 gibi) koşuldu ve SPIRENT_RUNNING_TEST_ID ile sonuçlar çekilebildi."""

    if spirent_running_test_id == 0:
        log.error('kiwi listener içerisinde spirent test id ye ulaşılamadı')
        sys.exit(110)

    processed_test_result = get_test_results(spirent_running_test_id)
    log.debug(f'Test result will be send to the Kiwi: {processed_test_result}')
    push_test_results_to_kiwi(kiwi_plan_id, kiwi_run_id, spirent_test_id, processed_test_result)
    log.info('Test result has been sent to the Kiwi')
# ------------------------------


class KiwiListener():

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.top_suite_name = None
        self.kiwi_run_id = None

    def start_suite(self, name, attributes):
        # Bir koşuda birden fazla test suit'in koşması istenirse her suite_start
        # Kiwi üzerinde yeni bir "Test Run" yaratmasın diye ilk "top_suite_name"
        # değişkeni kullanılacak.
        if self.top_suite_name is None:
            self.top_suite_name = name
            self.kiwi_run_id = create_test_run_on_kiwi()
            # Test koşusuna ortamdaki NF'leri sürümleriyle birlikte etiket olarak giriyoruz
            log.debug(f"{self.kiwi_run_id} ID'li tek bir Test Run oluşturuldu")

            if "DEFAULT_VERSION_PATH" in os.environ:
                version_file = os.environ['DEFAULT_VERSION_PATH']
                tag_responses = add_versions_as_tags(version_file, self.kiwi_run_id)
                log.debug(f"{self.kiwi_run_id} ID'li Test Run için versiyonlar etiket olarak eklendi {tag_responses}")

    def end_test(self, name, attributes):
        """"Her test başladığında SPIRENT_TEST_ID değeri ilgili *.robot testinde atanır.
        Her test sonlandığında bu SPIRENT_TEST_ID değerine göre test sonuçları çekilir"""
        log.debug(f"end_test > name: {name}  <>  attributes: {attributes}")
        spirent_test_id = BuiltIn().get_variable_value('${SPIRENT_TEST_ID}')  # robot dosyasının içinde varsa bu şekilde
        kiwi_plan_id = os.getenv('KIWI_PLAN_ID')
        # kiwi_plan_id = BuiltIn().get_variable_value('${KIWI_PLAN_ID}')
        spirent_running_test_id = BuiltIn().get_variable_value('${SPIRENT_RUNNING_TEST_ID}')
        send_test_result_to_kiwi(kiwi_plan_id, self.kiwi_run_id, spirent_test_id,
                                 spirent_running_test_id)  # başarılı oldu

    def end_suite(self, name, attributes):
        if name == self.top_suite_name:  # içine girince hatayı buradan verdi
            log.debug(f"{self.kiwi_run_id} ID'li tek bir Test Run BİTTİ")

    def close(self):
        pass
