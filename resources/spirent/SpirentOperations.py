from spirent.SpirentClient import SpirentClient
from globalProperties import *
from common.Logger import log
import json
import sys 
print("Python Version:", sys.version)
print("Python Executable Path:", sys.executable)
import jinja2
import sys

class SpirentOperations(SpirentClient):

    def __init__(self):
        super().__init__()

    def get_lib_id_mngr(self):
        get_lib_ids_response = self.get_libraries()
        if get_lib_ids_response:
            log.info('Spirent user={} library id received successfully'.format(SPIRENT_USER))
            all_libraries = get_lib_ids_response.json()
            if SPIRENT_USER in all_libraries.keys():
                return all_libraries[SPIRENT_USER]
            else:
                log.info('Spirent user={} not found!!'.format(SPIRENT_USER))
    
    def get_test_server_mngr(self,test_server_name_in):
        get_test_server_response = self.get_test_servers()        
        if get_test_server_response:
            all_test_servers = get_test_server_response.json()
            for each_test_server in all_test_servers['testServers']:
                print(each_test_server['name'])
                if each_test_server['name'] == test_server_name_in:
                    return each_test_server
                else:
                     log.error('Test server name={} not found!!'.format(test_server_name_in))

    def update_test_session_mngr(self,lib_id_in,test_name_in, update_test_session_data_in):      
        response = self.update_test_session(lib_id_in,test_name_in, json.loads(update_test_session_data_in))
        print("Test session update response={}".format(response.json()))
        return response.status_code

    def test_session_update_mngr(self,test_params_in, spirent_ts_param_in, amf_ip_in, upf_ip_in, h_mcc_in, h_mnc_in,
                             spirent_ts_name_in):
      """It is used to update spirent test session. To do this, it is important to create test session data properly.
      There is a template (jinja) which is named test_Session_template in the ./Resources/globalProperties.py
      This template is used to create test session data dynamically. According to the changing needs, test session
      data is created easily using below parameters.
      Ex:
      amf_info is used to modify AMF in the test session.
      ue_id is used to modify SUPI in the test session
      test_duration is used to specify when test is finished automatically.
       """
      self.sut_mngr(DEFAULT_SUT_NAME, amf_ip_in)
      lib_id = self.get_lib_id_mngr()
      test_server_id = self.get_test_server_mngr(spirent_ts_name_in)
      environment = jinja2.Environment()
      template = environment.from_string(test_Session_template)
      update_content = template.render(
        lib_id=lib_id,
        mnc_length=len(h_mnc_in),
        test_id=test_params_in['test_id'],
        test_duration=test_params_in['test_duration'],
        ts_id=test_server_id['id'],
        amf_info=DEFAULT_SUT_NAME,
        gnb_ip=spirent_ts_param_in['spirent_gnb_ip'],
        h_mcc=h_mcc_in,
        h_mnc=h_mnc_in,
        perm_key=test_params_in['perm_key'],
        op_key=test_params_in['op_key'],
        dn_ip=spirent_ts_param_in['spirent_dn_ip'],
        n6_ip=upf_ip_in,
        ue_id=h_mcc_in + h_mnc_in + test_params_in['msin'],
        dn_interface_info=spirent_ts_param_in['spirent_dn_interface'],
        gnb_interface_info=spirent_ts_param_in['spirent_gnb_interface']

      )
      print("Spirent test session update content:{}".format(update_content))
      return self.update_test_session_mngr(lib_id, test_params_in['test_id'], update_content)    
      
    def check_test_server(self,spirent_ts_name_in):
        """It is used to check spirent test server is ready or not. """
        test_server_state = self.get_test_server_mngr(spirent_ts_name_in)
        if test_server_state['state'] == "READY":
           print("[OK]Spirent test server is READY")
        else:
           sys.exit("[NOK]Test server is not READY!!Please check Spirent Test Server!!!")
           
    def sut_mngr(self,sut_name_in,amf_ip_in):
        get_sut_response = self.get_suts()        
        if get_sut_response:
            all_suts = get_sut_response.json()
            sut_found = False
            for each_sut in all_suts['suts']:             
                if each_sut['name'] == sut_name_in:
                    sut_found = True                  
                    sut_id = each_sut['id'] 
                    update_ts_data = dict()
                    update_ts_data.update({'ip': amf_ip_in})
                    update_sut_response = self.update_suts(sut_id,update_ts_data)
                    print("SUT update response={}".format(update_sut_response.json()))
            if not sut_found:
                    create_ts_data = dict()
                    create_ts_data.update({'ip': amf_ip_in})
                    create_ts_data.update({'managementIp': amf_ip_in})
                    create_ts_data.update({'type': 'GENERIC'})
                    create_ts_data.update({'name': sut_name_in})
                    create_sut_response = self.create_suts(create_ts_data)
                    print("SUT create response={}".format(create_sut_response.json()))

    def run_test_mngr(self, spirent_lib_id_in, test_name_in):
        run_test_data = dict()
        run_test_data.update({'library': spirent_lib_id_in,
                              'name': test_name_in})
        run_test_response = self.run_test(run_test_data)
        print(run_test_response.json())
        if run_test_response:
            running_test = run_test_response.json()
            print('Spirent test={} in user={} started successfully. Test run id='.format(test_name_in, SPIRENT_USER,running_test['id']))
            return running_test['id']

    def get_test_status_mngr(self, test_run_id_in):
        get_running_test_response = self.get_running_test(test_run_id_in)
        if get_running_test_response:
            print('Spirent test run={} running test status received successfully'.format(test_run_id_in))
            test_results = get_running_test_response.json()
            return test_results

    def get_test_results_mngr(self, test_run_id_in):
        get_test_results_response = self.get_test_results(test_run_id_in)
        if get_test_results_response:
            print('Spirent test run={} test results received successfully'.format(test_run_id_in))
            test_results = get_test_results_response.json()
            return test_results['criteria']

    def delete_test_run_mngr(self, test_run_id_in):
        return self.delete_test_run(test_run_id_in)





         
