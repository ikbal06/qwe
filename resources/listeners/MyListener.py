# MyListener.py

from common.Logger import log
import re
from robot.running.context import sys
from spirent.SpirentManager import SpirentManager
import os
from kiwi.KiwiClient import KiwiClient
from resources.common.Logger import log as logger
from robot.libraries.BuiltIn import BuiltIn
logger = BuiltIn()

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
    tr = _kc.testrun_create(kiwi_plan_id).get('result', {})
    tr_id = tr.get('id')
    if tr_id is None:
        log.error('Test koşu numarası None olamaz!')
        raise Exception('Test koşu numarası None olamaz!')
    return tr_id


def add_versions_as_tags(tr_id):
    file_path = 'version.txt'
    # TODO: Eğer dosya yoksa hata fırlat
    tags = _kc.get_tags(file_path) or []
    for t in tags:
        _kc.testrun_add_tag(tr_id, t)


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
            sys.exit(999)

        te = te[0]
        log.debug(f"> Brand new Test Execution created for {tc_id}: ", te)

        te_id = te["id"]
        # Test koşusuna eklediğimiz Test Senaryolarının durumlarını giriyoruz

        status_id = 4 if spirent_test_result["spirent_test_status"] == 'PASSED' else 5

        a = _kc.TestExecution_update(te_id, tr_id, tc_id, status_id)
        log.debug("Test Execution updated", a)
        comment = spirent_test_result["spirent_test_summary"]
        add_comment = _kc.TestExecution_add_comment(te_id, comment)
        return add_comment


def push_test_results_to_kiwi(tr_id, spirent_test_result):
    """"Kiwi üstünde Test Planına ait bir Test Koşusu (Test Run) yaratılacak (1).
    Test Koşusunda kullanılan NF'lerin adları ve sürümleri etiket (Tag) olarak koşuya eklenecek (2).
    Spirent Test Sonuçlarında Test Planının içindeki Test Senaryoları (Test Case) varsa,
    bu test senaryosu için Test Execution yaratılarak (3) testin sonucu Test Execution içinde güncellenecek (4).
    """
    # Test planı için bir test koşusu yaratıyoruz
    # plan_id = 1  # kiwi-testten bak bi ona göre düznele. bir de sışarıdan alacak şekilde olmlaı ya da en azından robot dosyasından

    # 1
    # tr_id = create_test_run_on_kiwi()

    # 2
    # Test koşusuna ortamdaki NF'leri sürümleriyle birlikte etiket olarak giriyoruz
    add_versions_as_tags(tr_id)

    # run için illa oradaki testleri mi koşmalıyız. eğer verilen test id yoksa oluşturulmalı(test case)
    # test planına eklenmeli ona göre yeni koşu oluşturmalıyız
    # ya da verilen plana göre içindeki test caselere bakılacak o test case varsa sadece o koşulaack
    # Test planındaki Test Senaryolarını -> Test koşusuna ekliyoruz
    # 3
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
        add_comment = _kc.TestExecution_add_comment(te_id, comment)
        return add_comment

    # for tc in cases:
    #     tc_id = tc["id"]
    #     tc_name = tc['summary']
    #     tc_names.append(tc_name)
    #     for tc_name in tc_names:
    #         if tc_name == spirent_test_id:
    #             te = _kc.TestRun_add_case(tr_id, tc_id)
    #             log.debug(f"> Brand new Test Execution created for {tc_id}: ")
    #             te_id = te["result"][0]["id"]
    #             # Test koşusuna eklediğimiz Test Senaryolarının durumlarını giriyoruz

    #             if spirent_test_result["spirent_test_status"] == 'PASSED':
    #                 status_id = 4
    #             else:
    #                 status_id = 5

    #             a = _kc.TestExecution_update(te_id, tr_id, tc_id, status_id)
    #             log.debug("Test Execution updated", a)
    #         else:
    #             log.debug(f'eklemek istediğiniz senaryo ({tc_name}) planda yok')

    # spirenttan gelen test adımları text olarak gelmeli statusleri ile birlikte


class MyListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3
    _tr_id = 0

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.top_suite_name = None
        logger.info('-----> __init__')

    def start_suite(self, name, attributes):
        logger.info(f'start_suite -----> {name}')

        if self.top_suite_name is None:

            self.top_suite_name = name

            logger.log_to_console(f"This is the top-level test: {name}")
        # Test süitine başlandığında yapılacak işlemler burada tanımlanır
        # TEST PLAN'ı için TEST RUN oluştur
        # Her end_test içinde Test Plan içindeki TEST CASE'lerden denk düşeni bu Test RUN'a sonucuyla ekle
        _tr_id = create_test_run_on_kiwi()

    def start_test(self, name, attributes):
        # Teste başlandığında yapılacak işlemler burada tanımlanır
        logger.log_to_console(f'start_test -----> {name}')

    def end_test(self, name, attributes):
        """"Test sonunda aşağıdaki işler yapılır:
        - Spirent test sonuçları çekilir
        - Kiwiye test sonuçları basılır"""
        logger.log_to_console(f'end_test -----> {name}')

        kiwi_plan_id = BuiltIn().get_variable_value('${KIWI_PLAN_ID}')
        spirent_test_id = BuiltIn().get_variable_value('${SPIRENT_TEST_ID}')
        spirent_running_test_id = BuiltIn().get_variable_value('${SPIRENT_RUNNING_TEST_ID}')
        if spirent_running_test_id == 0:
            log.error('kiwi listener içerisinde spirent test id ye ulaşılamadı')
            sys.exit(999)
        logger.debug(f"This is the top-level test: {name}")
        processed_test_result = get_test_results_for_kiwi(kiwi_plan_id, spirent_test_id, spirent_running_test_id)
        # push_test_results_to_kiwi(self._tr_id, processed_test_result)
        # log.log_to_console('Test result has been sent to the Kiwi')

    def end_suite(self, name, attributes, processed_test_result):
        logger.log_to_console(f'end_suite -----> {name}')

        logger.log_to_console(f'end_suite -- attributes -----> {attributes}')

        # if name == self.top_suite_name:

        # Bu bir en üst seviyedeki test ise, işlemlerinizi burada yapabilirsiniz.
        push_test_results_to_kiwi(self._tr_id, processed_test_result)
        log.log_to_console('Test result has been sent to the Kiwi')
