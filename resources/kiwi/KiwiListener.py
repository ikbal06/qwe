
import sys
from robot.libraries.BuiltIn import BuiltIn
from kiwi.KiwiClient import *
import os
from common.Logger import log
from spirent.SpirentManager import SpirentManager
import re

# ------------------------------

_kc = KiwiClient()


def get_test_results_for_kiwi(kiwi_plan_id, spirent_test_id, spirent_running_test_id):
    spirentManager = SpirentManager()
    # test_results = spirentManager.get_test_results_mngr(test_run_id_in=running_test_id)
    test_results = spirentManager.get_test_results_json(spirent_running_test_id)
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
        "kiwi_plan_id": kiwi_plan_id,
        "spirent_test_id": spirent_test_id,  # kt_cn_001
        "spirent_running_test_id": spirent_running_test_id,  # spirentta o an koşan testin nosu
        "spirent_test_summary": '\n'.join(test_results_for_kiwi),
        "spirent_test_status": all_test_status
    }


def create_test_run_on_kiwi():
    # 1
    kiwi_plan_id = BuiltIn().get_variable_value('${KIWI_PLAN_ID}')
    tr = _kc.TestRun_create(kiwi_plan_id).get('result', {})
    log.debug(f'Test koşusu yaratıldı: {tr}')

    tr_id = tr.get('id')
    if tr_id is None:
        log.error('Test koşu numarası None olamaz!')
        raise Exception('Test koşu numarası None olamaz!')

    log.debug(f'Test koşusu {tr_id} ID değeriyle oluşturuldu')
    return tr_id


def add_versions_as_tags(tr_id):
    file_path = 'version.txt'
    # TODO: Eğer dosya yoksa hata fırlat.masın da warning göndersin etiket olarka test adı?
    tags = _kc.get_tags(file_path) or []

    if tags == []:
        log.info('tag için uygun dosya bulunamadı')
        _kc.TestRun_add_tag(tr_id, 'tagyok')

    for t in tags:
        _kc.TestRun_add_tag(tr_id, t)


def add_test_case_into_run(spirent_test_result, tr_id):
    spirent_test_id = BuiltIn().get_variable_value('${SPIRENT_TEST_ID}')
    kiwi_plan_id = BuiltIn().get_variable_value('${KIWI_PLAN_ID}')
    tc_names = []
    cases = _kc.get_TestCase_by_plan_id(kiwi_plan_id).get('result', [])
    found_cases = [tc for tc in cases if tc['summary'] == spirent_test_id]
    if len(found_cases) > 0:
        tc = found_cases[0]
        tc_id = tc['id']
        te = _kc.TestRun_add_case(tr_id, tc_id).get('result', [])

        if len(te) == 0:
            log.error(f"Test Execution could not created")
            sys.exit(109)

        te = te[0]
        log.debug(f"> Brand new Test Execution created for {tc_id} ")

        te_id = te["id"]
        # Test koşusuna eklediğimiz Test Senaryolarının durumlarını giriyoruz

        status_id = 4 if spirent_test_result["spirent_test_status"] == 'PASSED' else 5

        a = _kc.TestExecution_update(te_id, tr_id, tc_id, status_id)
        log.debug(f"Test Execution updated {a}")
        comment = spirent_test_result["spirent_test_summary"]
        add_comment = _kc.TestExecution_add_comment(te_id, comment)
        return add_comment


def push_test_results_to_kiwi(tr_id, spirent_test_result):
    """"Kiwi üstünde Test Planına ait bir Test Koşusu (Test Run) yaratılacak (1).
    Test Koşusunda kullanılan NF'lerin adları ve sürümleri etiket (Tag) olarak koşuya eklenecek (2).
    Spirent Test Sonuçlarında Test Planının içindeki Test Senaryoları (Test Case) varsa,
    bu test senaryosu için Test Execution yaratılarak (3) testin sonucu Test Execution içinde güncellenecek (4).
    """
    # Test koşusuna ortamdaki NF'leri sürümleriyle birlikte etiket olarak giriyoruz
    add_versions_as_tags(tr_id)

    # Test planındaki Test Senaryolarını -> Test koşusuna ekliyoruz
    add_test_case_into_run(spirent_test_result, tr_id)


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


def send_test_reult_to_kiwi(self, name):
    kiwi_plan_id = BuiltIn().get_variable_value('${KIWI_PLAN_ID}')
    spirent_test_id = BuiltIn().get_variable_value('${SPIRENT_TEST_ID}')
    spirent_running_test_id = BuiltIn().get_variable_value('${SPIRENT_RUNNING_TEST_ID}')
    if spirent_running_test_id == 0:
        log.error('kiwi listener içerisinde spirent test id ye ulaşılamadı')
        sys.exit(110)
    log.debug(f"This is the top-level test: {name}")
    processed_test_result = get_test_results_for_kiwi(kiwi_plan_id, spirent_test_id, spirent_running_test_id)
    log.debug('Test result has been sent to the Kiwi')
    push_test_results_to_kiwi(self.kiwi_run_id, processed_test_result)
    log.info('Test result has been sent to the Kiwi')
# ------------------------------


class KiwiListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.top_suite_name = None
        self.kiwi_run_id = None

    def start_suite(self, name, attributes):
        if "DEFAULT_VERSION_PATH" in os.environ:
            self.version_file = os.environ['DEFAULT_VERSION_PATH']
            log.debug("self.version_file: ", self.version_file)

        if self.top_suite_name is None:
            self.top_suite_name = name
            self.kiwi_run_id = create_test_run_on_kiwi()

    def end_test(self, name, attributes):
        log.debug(f"end_test {name} {attributes}")
        # send_test_result_to_kiwi()

    def end_suite(self, name, attributes):
        if name == self.top_suite_name:
            log.debug(f"This is the top-level test: {name}")

    def close(self):
        pass
