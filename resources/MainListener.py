import time
import os
import subprocess
from pathlib import Path
from robot.libraries.BuiltIn import BuiltIn
from EnvDataOperations import *
from TestConfigOperations import *
from spirent.SpirentOperations import SpirentOperations
from globalProperties import *


class MainListener:

    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    def _start_suite(self, data, test):

        data.tests.clear()
        current_suite = data
        test_id = BuiltIn().get_variable_value("${TEST_ID}")        
        new_suite = data.suites.create(name=test_id)      
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
           print(response_status_code)
           if response_status_code == 200:
              print("[OK] Test session update operation SUCCESSFULL!!!")                 
              spirent_lib_id = SpirentOperations().get_lib_id_mngr()
              if spirent_lib_id:
                 self.test_run_id = SpirentOperations().run_test_mngr(spirent_lib_id, test_id)
                 test_start_time = time.time()
                 if self.test_run_id:
                    print('Spirent test={} test run id={}'.format(test_id, self.test_run_id))
                    while time.time() < test_start_time + 1800:
                       time.sleep(10)
                       running_test_status = SpirentOperations().get_test_status_mngr(self.test_run_id)
                       if running_test_status['testStateOrStep'] == "COMPLETE" or running_test_status['testStateOrStep'] == "COMPLETE_ERROR":
                          break
            
                    if running_test_status:
                    
                       self.spirent_report_urls = running_test_status["resultFilesList"]
                       test_results = SpirentOperations().get_test_results_mngr(self.test_run_id)
                       os.environ[test_id] = "PASSED"
                       for each_step in test_results:
                           test_desc = each_step["description"]
                           test_status = each_step["status"]
                           test_step_name = test_desc[test_desc.find("(") + 1:test_desc.find(")")]
                           print('Spirent test={} test step={} test status={}'.format(test_id, test_step_name, test_status))
                           tc = new_suite.tests.create(name=test_step_name, tags=test_id)
                           tc.body.create_keyword(name="Should Be Equal As Strings", args=["PASSED", test_status])
                           if test_status == "FAILED":
                              os.environ[test_id] = "FAILED"
                    else:
                        print('Spirent test={} results not received!!'.format(test_id))
                 else:
                     print('Spirent test={} not started!!'.format(test_id))
              else:
                print('Spirent user lib id not received!!')
           else:
              print("[NOK] Spirent test session update failed for {}. NO RUN TEST!!!".format(each_test_id))
        else:
              print("[NOK]Test parameters or spirent ts parameters are not found for {} and {}. Please provide it to globalProperties file".format(each_test_id, env_data_obj.spirent_ts_name))

    def _end_suite(self, name, attrs):
     
            if self.test_run_id:
               if not os.path.exists(self.spirent_report_path):
                  print('Spirent report path={} not found. Create..'.format(self.spirent_report_path))
                  Path(self.spirent_report_path).mkdir(parents=True, exist_ok=True, mode=0o755)
            
               for eachURL in self.spirent_report_urls:
                    try:
                        subprocess.call("wget " + eachURL + " -P " + self.spirent_report_path, shell=True)
                        print('Spirent report={} received'.format(eachURL))
                    except Exception as e:
                        print('Spirent report={} not received. Error={}'.format(eachURL,e))

               SpirentOperations().delete_test_run_mngr(self.test_run_id)

            

