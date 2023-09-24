import sys
import jinja2
from resources.spirent.SpirentClient import SpirentClient
from resources.globalProperties import *
from resources.common.Logger import log
import json
import sys


class SpirentManager(SpirentClient):

    def __init__(self):
        super().__init__()

    def update_test_server_session_or_exit(
            self, test_id, amf_ip, upf_ip, test_duration, spirent_ts_name, spirent_ts_id, spirent_gnb_ip,
            spirent_dn_ip, spirent_dn_interface, spirent_gnb_interface, h_mnc, h_mcc, perm_key, op_key, msin):
        '''Spirent Test Sunucusu üzerinde bir test oturumu yaratacağız. 
        Bu oturumda kullanılmak üzere bazı bilgileri güncelleyeceğiz.
        Örneği MNC, MCC, AMF IP vs.
        '''
        self.update_or_create_spirent_sut_by_name(DEFAULT_SUT_NAME, amf_ip)
        lib_id = self.get_library_id_by_spirent_user_or_exit()
        # test_server = self.get_test_server_mngr(spirent_ts_name)
        test_server = self.get_test_server_or_exit(spirent_ts_name)
        update_content = self.render_test_session_template(
            test_id, lib_id, h_mnc, h_mcc, test_duration, spirent_ts_id, spirent_gnb_ip, perm_key, op_key,
            spirent_dn_ip, upf_ip, msin, spirent_dn_interface, spirent_gnb_interface)
        if update_content:
            spirent_update_data = json.loads(update_content)
            log.debug("Spirent Test About To Be Updated", spirent_update_data)
            response = self.update_test_session(lib_id, test_id, spirent_update_data)
            response_data = response.json()
            if response.status_code != 200:
                log.error(f'Test session güncellenemedi! Sunucu Cevabı: {response_data}')
                sys.exit(108)
            else:
                log.debug(f"{response_data['url']} Testi güncellendi: {response_data}")
                return response_data
        else:
            log.error(f'Test session güncelleme verisi geçersiz olduğu için güncellenemedi: {update_content}')
            sys.exit(108)

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

    def get_library_id_by_spirent_user_or_exit(self, spirent_user=SPIRENT_USER):
        response = self.get_libraries()
        if response.status_code != 200:
            log.error(f'Spirent user={spirent_user} library id could not received!')
            sys.exit(106)

        response_json = response.json()
        log.debug(f'Spirent Library Id Çekildi', response_json)

        lib_id = response_json.get(spirent_user)
        if not lib_id:
            log.error("Spirent Library Id değeri boş olamaz")
            sys.exit(101)

        log.debug(f'Spirent user={spirent_user} library id ({lib_id}) received successfully')
        return lib_id

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

    def render_test_session_template(
            self, test_id, lib_id, h_mnc, h_mcc, test_duration, spirent_ts_id, spirent_gnb_ip,
            perm_key, op_key, spirent_dn_ip, upf_ip, msin, spirent_dn_interface, spirent_gnb_interface):

        template_data = {
            'lib_id': lib_id,
            'mnc_length': len(h_mnc),  # len(test_params['h_mnc']),
            'test_id': test_id,  # test_params['test_id'],
            'test_duration': test_duration,  # test_params['test_duration'],
            'amf_info': DEFAULT_SUT_NAME,
            'h_mcc':  h_mcc,  # test_params['h_mcc'],
            'h_mnc':  h_mnc,  # test_params['h_mnc'],
            'perm_key': perm_key,  # test_params['perm_key'],
            'op_key': op_key,  # test_params['op_key'],
            'ue_id': h_mcc + h_mnc + msin,  # test_params['h_mcc'] + test_params['h_mnc'] + test_params['msin'],
            'ts_id': spirent_ts_id,  # spirent_ts_param['id'],
            'gnb_ip': spirent_gnb_ip,  # spirent_ts_param['spirent_gnb_ip'],
            'dn_ip': spirent_dn_ip,  # spirent_ts_param['spirent_dn_ip'],
            'dn_interface_info': spirent_dn_interface,  # spirent_ts_param['spirent_dn_interface'],
            'gnb_interface_info': spirent_gnb_interface,  # spirent_ts_param['spirent_gnb_interface'],
            'n6_ip': upf_ip,  # test_params['upf_ip'],
        }
        environment = jinja2.Environment()
        template = environment.from_string(test_Session_template)
        return template.render(**template_data)

    def run_test_on_spirent(self, spirent_lib_id_in, test_name):
        data = {'library': spirent_lib_id_in, 'name': test_name}
        log.debug("Test Run is about to run", data)
        response = self.run_test(data)

        if not response:
            log.error("Response from the server couldn't retrieved")
            sys.exit(444)

        response_data = response.json()
        if response.status_code != 201:
            log.debug("Test Initialization Failed", {"girdi": data, "sonuc": response_data})
            log.error("Test failed to start!")
            sys.exit(333)

        log.debug(f"Test Run has started [{response.status_code}]", response_data)
        test_id = response_data['id']
        log.debug(f"Spirent test={test_name} in user={SPIRENT_USER} started successfully. Test run id={test_id}")
        return test_id

    def get_test_status(self, test_id):
        response = self.get_running_test(test_id)
        if response.status_code != 200:
            log.warning('Test sonucu çekilemedi!')
            return None

        log.debug(f'Spirent test run={test_id} running test status received successfully')
        test_results = response.json()
        return test_results
# -----------------------------------------------------

    def get_spirent_test_servers(self):
        response = self.get_test_servers()
        if response.status_code != 200:
            log.warning("Spirent sunucu bilgilerine erişilemedi!")
            sys.exit(102)

        return response.json().get('testServers')

    def get_spirent_test_server_by_name(self, server_name):
        """Spirent üzerinden Test Sunucularından server_name ile verilen test sunucusunun bilgisi çekilir.

        Args:
            server_name (str): Spirent test sunucusunun adı

        Returns:
            dict: Sunucu ayrıntıları

        ```json

        {
        'url': 'http://10.10.20.74:8080/api/testServers/1',
        'id': 1,
        'name': 'vts-VTO2',
        'state': 'READY',
        'version': '20.6.1.9'
        }
        """
        for server in self.get_spirent_test_servers():
            if server['name'] == server_name:
                log.debug(f"Spirent Test Sunucusunun Bilgileri Çekildi",  server)
                return server
            else:
                log.error(f'Test server name={server_name} not found!!')
                sys.exit(103)

# -----------------------------------------------------
# -----------------------------------------------------
    def get_lib_id_mngr(self):
        get_lib_ids_response = self.get_libraries()
        if get_lib_ids_response:
            log.info(
                'Spirent user={} library id received successfully'.format(SPIRENT_USER))
            all_libraries = get_lib_ids_response.json()
            if SPIRENT_USER in all_libraries.keys():
                return all_libraries[SPIRENT_USER]
            else:
                log.info('Spirent user={} not found!!'.format(SPIRENT_USER))

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

    def update_test_session_mngr(self, lib_id_in, test_name_in, update_test_session_data_in):
        response = self.update_test_session(
            lib_id_in, test_name_in, json.loads(update_test_session_data_in))
        print("Test session update response={}".format(response.json()))
        return response.status_code

    def test_session_update_mngr(self, test_params_in, spirent_ts_param_in, amf_ip_in, upf_ip_in, h_mcc_in, h_mnc_in,
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
        test_server_id = self.get_test_server_mngr(spirent_ts_name_in)
        lib_id = self.get_lib_id_mngr()
        template = jinja2.Environment().from_string(test_Session_template)
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
            gnb_interface_info=spirent_ts_param_in['spirent_gnb_interface'])

        log.debug("Spirent test session update content: ", update_content)
        return self.update_test_session_mngr(lib_id, test_params_in['test_id'], update_content)

    def check_test_server(self, spirent_ts_name_in):
        """It is used to check spirent test server is ready or not. """
        test_server_state = self.get_test_server_mngr(spirent_ts_name_in)
        if test_server_state['state'] == "READY":
            log.debug("[OK]Spirent test server is READY")
            return True
        else:
            msg = "[NOK]Test server is not READY!!Please check Spirent Test Server!!!"
            log.error(msg)
            return False
            sys.exit(msg)

    def sut_mngr(self, sut_name_in, amf_ip_in):
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
                    update_sut_response = self.update_suts(
                        sut_id, update_ts_data)
                    print("SUT update response={}".format(
                        update_sut_response.json()))
            if not sut_found:
                create_ts_data = dict()
                create_ts_data.update({'ip': amf_ip_in})
                create_ts_data.update({'managementIp': amf_ip_in})
                create_ts_data.update({'type': 'GENERIC'})
                create_ts_data.update({'name': sut_name_in})
                create_sut_response = self.create_suts(create_ts_data)
                print("SUT create response={}".format(
                    create_sut_response.json()))

    def run_test_mngr(self, spirent_lib_id_in, test_name_in):
        run_test_data = dict()
        run_test_data.update({'library': spirent_lib_id_in,
                              'name': test_name_in})
        run_test_response = self.run_test(run_test_data)
        print(run_test_response.json())
        if run_test_response:
            running_test = run_test_response.json()
            print('Spirent test={} in user={} started successfully. Test run id='.format(
                test_name_in, SPIRENT_USER, running_test['id']))
            return running_test['id']

    def get_test_status_mngr(self, test_run_id_in):
        get_running_test_response = self.get_running_test(test_run_id_in)
        if get_running_test_response:
            print('Spirent test run={} running test status received successfully'.format(
                test_run_id_in))
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
