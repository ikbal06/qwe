import time
import os
import subprocess
from pathlib import Path
from robot.libraries.BuiltIn import BuiltIn
from EnvDataOperations import *
from TestConfigOperations import *
from spirent.SpirentOperations import SpirentOperations
from globalProperties import *
# from common.Logger import robot_logger as log
from common.Logger import log


class MainListener:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        log.debug('This is a debug message.')

    def start_test(self, name, attrs):
        log.info(f"Test started")

    def end_test(self, name, attrs):
        log.info(f"Test ended")

    def start_suite(self, suite, test):
        self.suite_source = BuiltIn().get_variable_value('${SUITE SOURCE}')
        log.info(f"Test suite started:")

        # data.tests.clear()
        test_id = BuiltIn().get_variable_value("${TEST_ID}")
        new_suite = suite.suites.create(name=test_id)
        self.env_variables = EnvDataOperations()
        self.spirent_report_path = BuiltIn().get_variable_value("${DEFAULT_TEST_LOGS_PATH}")
        test_param = TestConfigOperations(test_name=test_id).get_test_params()
        spirent_ts_param = TestConfigOperations(ts_name=self.env_variables.spirent_ts_name).get_spirent_ts_params()

        if test_param and spirent_ts_param:
            response_status_code = SpirentOperations().test_session_update_mngr(test_param,
                                                                                spirent_ts_param,
                                                                                self.env_variables.public_ip,
                                                                                self.env_variables.n6_ip,
                                                                                self.env_variables.h_mcc,
                                                                                self.env_variables.h_mnc,
                                                                                self.env_variables.spirent_ts_name)
            log.info(f'Spirent test sonuçları durum kodu: {response_status_code}')
            if response_status_code == 200:
                log.info("[OK] Test session update operation SUCCESSFULL!!!")
                spirent_lib_id = SpirentOperations().get_lib_id_mngr()
                if spirent_lib_id:
                    self.test_run_id = SpirentOperations().run_test_mngr(spirent_lib_id, test_id)
                    test_start_time = time.time()
                    if self.test_run_id:
                        log.info(f'Spirent test={test_id} test run id={self.test_run_id}')
                        while time.time() < test_start_time + 1800:
                            time.sleep(10)
                            running_test_status = SpirentOperations().get_test_status_mngr(self.test_run_id)
                            is_test_completed = running_test_status['testStateOrStep'] == "COMPLETE"
                            is_test_completed_with_error = running_test_status['testStateOrStep'] == "COMPLETE_ERROR"

                            # Her iki durumda da döngüyü sonlandırın
                            if is_test_completed or is_test_completed_with_error:
                                break

                        if running_test_status:

                            self.spirent_report_urls = running_test_status["resultFilesList"]
                            test_results = SpirentOperations().get_test_results_mngr(self.test_run_id)
                            os.environ[test_id] = "PASSED"
                            for each_step in test_results:
                                test_desc = each_step["description"]
                                test_status = each_step["status"]
                                test_step_name = test_desc[te_desc.find("(") + 1:test_desc.find(")")]
                                tc = new_suite.tests.create(
                                    name=test_step_name, tags=test_id)
                                log.info(f'Spirent test={test_id} test step={test_step_name} test status={test_status}')
                                tc.body.create_keyword(name="Should Be Equal As Strings", args=["PASSED", test_status])
                                if test_status == "FAILED":
                                    os.environ[test_id] = "FAILED"
                        else:
                            log.info(
                                f'Spirent test={test_id} results not received!!')
                    else:
                        log.info(f'Spirent test={test_id} not started!!')
                else:
                    log.info('Spirent user lib id not received!!')
            else:
                log.info(
                    f"[NOK] Spirent test session update failed for {each_test_id}. NO RUN TEST!!!")
        else:
            log.info(
                f'[NOK]Test parameters or spirent ts parameters are not found for {each_test_id} and {env_data_obj.spirent_ts_name}. Please provide it to globalProperties file')

    def end_suite(self, suite, attrs):
        log.info(f"Test suite ended: {suite}")

        if self.test_run_id:
            if not os.path.exists(self.spirent_report_path):
                log.info(
                    f'Spirent report path={self.spirent_report_path} not found. Create..')
                Path(self.spirent_report_path).mkdir(
                    parents=True, exist_ok=True, mode=0o755)

            for eachURL in self.spirent_report_urls:
                try:
                    subprocess.call("wget " + eachURL + " -P " +
                                    self.spirent_report_path, shell=True)
                    log.info(f'Spirent report={eachURL} received')
                except Exception as e:
                    log.info(f'Spirent report={eachURL} not received. Error={e}')

            SpirentOperations().delete_test_run_mngr(self.test_run_id)


if __name__ == "__main__":
    # mListener = MainListener()
    pass
