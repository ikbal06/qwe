import sys
import jinja2
from robot.libraries.BuiltIn import BuiltIn
from EnvDataOperations import EnvDataOperations
from TestConfigOperations import TestConfigOperations
from resources.spirent.SpirentClient import SpirentClient
from resources.globalProperties import *
from resources.common.Logger import log
import json
import sys
print("Python Version:", sys.version)
print("Python Executable Path:", sys.executable)


class SpirentManager(SpirentClient):

    def __init__(self):
        super().__init__()

    def update_test_session_c2(self, test_name=None, ts_name=None):
        content = self.prepare_update_content(test_name, ts_name)
        response = update_session(content)
        if response['status_code'] == 200:
            log.debug('')
            return True
        else:
            log.warning(f'Güncellenemedi: ${response.json()}')
            return False

    def prepare_update_content(self, test_name=None, ts_name=None):
        # Değerleri getir
        # Şablonu render et
        config = TestConfigOperations(test_name, ts_name)
        test_params = config.get_test_params()
        ts_params = config.get_spirent_ts_params

        env = EnvDataOperations()
        if test_params and ts_params:
            self.sut_mngr(DEFAULT_SUT_NAME, amf_ip_in)
            test_id = test_params_in['test_id']
            test_name = test_params_in['test_id']
            test_server_id = self.get_test_server_mngr(spirent_ts_name_in)
            lib_id = self.get_lib_id()
            try:
                template = jinja2.Environment().from_string(test_Session_template)
                update_content = template.render(
                    lib_id=lib_id,
                    mnc_length=len(h_mnc_in),
                    test_id=test_id,
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
                    gnb_interface_info=spirent_ts_param_in['spirent_gnb_interface'])
            except:
                log.error('Jinja şablonu işlenemedi!')
                sys.exit(333)

            log.debug("Spirent test session update content: ${update_content}")

            log.debug(f'Spirent test sonuçları durum kodu: {response_status_code}')

            if response_status_code == 200:
                log.debug("[OK] Test session update operation SUCCESSFULL!!!")
            else:
                log.warning(f'Spirent test sonuçları durum kodu: {response_status_code}')

    def update_test_session_c(self, test_name=None, ts_name=None):
        '''
        Spirent test oturumunu koşulacak teste ve koşulacak ortama göre ayarlar:
        - güncellenecek veriyi hazırla
        - spirent'ı güncelle
        '''
        config = TestConfigOperations(test_name, ts_name)
        test_params = config.get_test_params()
        ts_params = config.get_spirent_ts_params

        env = EnvDataOperations()
        self.spirent_report_path = BuiltIn().get_variable_value("${DEFAULT_TEST_LOGS_PATH}")

        if test_params and ts_params:
            response_status_code = self.test_session_update_mngr(test_params,
                                                                 ts_params,
                                                                 env.public_ip,
                                                                 env.n6_ip,
                                                                 env.h_mcc,
                                                                 env.h_mnc,
                                                                 env.spirent_ts_name)
            log.debug(f'Spirent test sonuçları durum kodu: {response_status_code}')

            if response_status_code == 200:
                log.debug("[OK] Test session update operation SUCCESSFULL!!!")
            else:
                log.warning(f'Spirent test sonuçları durum kodu: {response_status_code}')

    def run_tests(self):
        pass

    # def get_lib_id_mngr(self):
    #     get_lib_ids_response = self.get_libraries()
    #     if get_lib_ids_response:
    #         log.info(
    #             'Spirent user={} library id received successfully'.format(SPIRENT_USER))
    #         all_libraries = get_lib_ids_response.json()
    #         if SPIRENT_USER in all_libraries.keys():
    #             return all_libraries[SPIRENT_USER]
    #         else:
    #             log.info('Spirent user={} not found!!'.format(SPIRENT_USER))

    def get_test_server_mngr(self, test_server_name_in):
        get_test_server_response = self.get_test_servers()
        if get_test_server_response:
            all_test_servers = get_test_server_response.json()
            for each_test_server in all_test_servers['testServers']:
                log.debug(each_test_server['name'])
                if each_test_server['name'] == test_server_name_in:
                    return each_test_server
                else:
                    log.error('Test server name={} not found!!'.format(
                        test_server_name_in))

    def c(self,
          test_params_in,
          spirent_ts_param_in,
          amf_ip_in,
          upf_ip_in,
          h_mcc_in,
          h_mnc_in,
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
        test_id = test_params_in['test_id']
        test_name = test_params_in['test_id']
        test_server_id = self.get_test_server_mngr(spirent_ts_name_in)
        lib_id = self.get_lib_id()
        try:
            template = jinja2.Environment().from_string(test_Session_template)
            update_content = template.render(
                lib_id=lib_id,
                mnc_length=len(h_mnc_in),
                test_id=test_id,
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
                gnb_interface_info=spirent_ts_param_in['spirent_gnb_interface'])
        except:
            log.error('Jinja şablonu işlenemedi!')
            sys.exit(333)

        log.debug("Spirent test session update content: ${update_content}")

        response = self.update_test_session(
            lib_id,
            test_name,
            json.loads(update_content)
        )
        log.debug(f"Test session update response={response.json()}")
        return response.status_code

    def check_test_server(self, spirent_ts_name):
        """It is used to check spirent test server is ready or not. """
        test_server_state = self.get_test_server_mngr(spirent_ts_name)
        if test_server_state['state'] == "READY":
            log.debug("[OK]Spirent test server is READY")
            return True
        else:
            msg = "[NOK]Test server is not READY!!Please check Spirent Test Server!!!"
            log.error(msg)
            return False
            sys.exit(msg)

    def _get_spirent_sut_by_name(self, sut_name):
        """"Spirent taranfında SUT bilgisini sut adına göre çekiyoruz. 
        Eğer bu isimde sut bulunamazsa None dönüyoruz """
        get_sut_response = self.get_suts()
        if get_sut_response:
            all_suts = get_sut_response.json()
            for sut in all_suts['suts']:
                if sut['name'] == sut_name:
                    return sut
        return None

    def _update_sut_amf_id(self, sut_name, amf_ip):
        """"Spirent taranfında SUT oluşturmak için kullanıyoruz"""
        sut = self._get_spirent_sut_by_name(sut_name)
        sut_id = sut['id']
        update_ts_data = dict()
        update_ts_data.update({'ip': amf_ip})
        update_sut_response = self.update_suts(sut_id, update_ts_data)
        log.debug(f"SUT updated", update_sut_response)

    def _create_spirent_sut(self, sut_name, amf_ip):
        create_ts_data = dict()
        create_ts_data.update({'ip': amf_ip})
        create_ts_data.update({'managementIp': amf_ip})
        create_ts_data.update({'type': 'GENERIC'})
        create_ts_data.update({'name': sut_name})
        create_sut_response = self.create_suts(create_ts_data)
        log.debug("SUT created ", create_sut_response.json())

    def update_or_create_spirent_sut_by_name(self, sut_name, amf_ip):
        '''SUT Bilgisini Spirent üzerinden hedef AMF IP bilgisi ile güncelliyoruz.
        Böylece testler AMF'in bulunduğu çekirdek şebekeye doğru koşulacak'''
        if self._get_spirent_sut_by_name(sut_name):
            self._update_sut_amf_id(sut_name, amf_ip)
        else:
            self._create_spirent_sut(sut_name, amf_ip)

    # def run_spirent_test(self, spirent_lib_id, test_name):
    #     data = {'library': spirent_lib_id, 'name': test_name}
    #     response = self.run_test(data)
    #     print(response.json())
    #     if response.status_code != 200:
    #         log.error("Spirent güncellenemedi!")
    #         sys.exit(105)

    #     running_test_id = response.json().get('id')
    #     job = {
    #         "Spirent User": SPIRENT_USER,
    #         "Test Name": test_name,
    #         "Test ID": running_test_id
    #     }
    #     log.debug('Spirent test started successfully.', job)
    #     return running_test_id

    def get_test_status_mngr(self, test_run_id):
        get_running_test_response = self.get_running_test(test_run_id)
        if get_running_test_response:
            print('Spirent test run={} running test status received successfully'.format(
                test_run_id))
            test_results = get_running_test_response.json()
            return test_results

    def get_test_results_mngr(self, test_run_id_in):
        get_test_results_response = self.get_test_results(test_run_id_in)
        if get_test_results_response:
            print('Spirent test run={} test results received successfully'.format(
                test_run_id_in))
            test_results = get_test_results_response.json()
            return test_results['criteria']

    def delete_test_run_mngr(self, test_run_id_in):
        return self.delete_test_run(test_run_id_in)


# ---------------------------------------------------------------------------------


    def get_spirent_test_servers(self):
        response = self.get_test_servers()
        if response.status_code != 200:
            log.warning("Spirent sunucu bilgilerine erişilemedi!")
            sys.exit(102)

        return response.json().get('testServers')

    def get_spirent_test_server_by_name(self, server_name):
        for server in self.get_spirent_test_servers():
            if server['name'] == server_name:
                log.debug("Spirent Test Sunucusu bulundu",  server)
                return server
            else:
                log.error(f'Test server name={server_name} not found!!')
                sys.exit(103)

    def get_test_server_or_exit(self, test_server_name):
        get_test_server_response = self.get_test_servers()

        if get_test_server_response.status_code != 200:
            log.error(f"Failed to retrieve test servers. Status code: {get_test_server_response.status_code}")
            sys.exit(102)
        else:
            all_test_servers = get_test_server_response.json().get('testServers', [])
            for test_server in all_test_servers:
                if test_server.get('name') == test_server_name:
                    return test_server

        log.error(f"Test server with name '{test_server_name}' not found.")
        sys.exit(103)

    def run_test_or_exit(self, spirent_lib_id, test_name):
        """"Bu fonksiyon Spirent üsütünde verilen testi koşar ve testin id değerini döner veya programdan çıkış yapar"""
        run_test_data = {
            'library': spirent_lib_id,
            'name': test_name
        }
        run_test_response = self.run_test(run_test_data)

        if run_test_response.status_code != 200:
            log.error(f'Failed to start Spirent test={test_name}. Status code: {run_test_response.status_code}')
            sys.exit(104)
        else:
            test_run_id = run_test_response.json().get('id')

            test_info = {
                "Spirent User": SPIRENT_USER,
                "Test Name": test_name,
                "Run Id": test_run_id
            }
            log.custom_debug("SPIRENT TEST STARTED", test_info)
            return test_run_id

    def render_test_session_template(self, lib_id, test_params, spirent_ts_param):
        template_data = {
            'lib_id': lib_id,
            'mnc_length': len(test_params['h_mnc']),
            'test_id': test_params['test_id'],
            'test_duration': test_params['test_duration'],
            'ts_id': spirent_ts_param['id'],
            'amf_info': DEFAULT_SUT_NAME,
            'gnb_ip': spirent_ts_param['spirent_gnb_ip'],
            'h_mcc': test_params['h_mcc'],
            'h_mnc': test_params['h_mnc'],
            'perm_key': test_params['perm_key'],
            'op_key': test_params['op_key'],
            'dn_ip': spirent_ts_param['spirent_dn_ip'],
            'n6_ip': test_params['upf_ip'],
            'ue_id': test_params['h_mcc'] + test_params['h_mnc'] + test_params['msin'],
            'dn_interface_info': spirent_ts_param['spirent_dn_interface'],
            'gnb_interface_info': spirent_ts_param['spirent_gnb_interface']
        }
        environment = jinja2.Environment()
        template = environment.from_string(test_Session_template)
        return template.render(**template_data)

    def get_library_id_or_exit(self):
        response = self.get_libraries()
        if response.status_code != 200:
            log.error(f'Spirent user={SPIRENT_USER} library id could not received!')
            sys.exit(106)

        lib_id = response.json().get(SPIRENT_USER)
        if not lib_id:
            log.error("Spirent Library Id değeri boş olamaz")
            sys.exit(101)

        log.debug(f'Spirent user={SPIRENT_USER} library id ({lib_id}) received successfully')
        return lib_id

    def update_test_session(self, lib_id, test_name, update_test_session_data):
        response = self.update_test_session(lib_id, test_name, json.loads(update_test_session_data))
        if response.status_code != 200:
            sys.exit(107)
        data = {
            'Spirent User': SPIRENT_USER,
            'User Library ID': lib_id,
            'Test Name': test_name,
            'Response': response.json()
        }
        log.debug(f'Test session updated', data)
        return response.status_code

    def update_test_server_session(
            self, test_params, spirent_ts_param, amf_ip, dn_ip, h_mcc, h_mnc, spirent_ts_name):
        '''Spirent Test Sunucusu üzerinde bir test oturumu yaratacağız. 
        Bu oturumda kullanılmak üzere bazı bilgileri güncelleyeceğiz.
        Örneği MNC, MCC, AMF IP vs.
        '''
        self.update_or_create_spirent_sut_by_name(DEFAULT_SUT_NAME, amf_ip)
        lib_id = self.get_library_id_or_exit()
        test_server = self.get_test_server_mngr(spirent_ts_name)
        update_content = self.render_test_session_template(lib_id, test_params, spirent_ts_param)
        if update_content:
            log.debug("Spirent test session update content: ", update_content)
            return self.update_test_session(lib_id, test_params['test_id'], update_content)
        else:
            log.error(f'Test session güncellenemedi')
            sys.exit(108)
