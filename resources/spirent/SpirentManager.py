import sys
import jinja2
import json
import sys
from resources.spirent.SpirentClient import SpirentClient
from resources.globalProperties import *
from resources.common.Logger import log


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

    def get_test_results_by_id(self, test_run_id_in):
        response = self.get_test_results(test_run_id_in)
        if response:
            print('Spirent test run={} test results received successfully'.format(
                test_run_id_in))
            test_results = response.json()
            return test_results

    def get_test_results_json(self, test_run_id):
        response = self.get_test_results(test_run_id)
        if response.status_code != 200:
            log.error(f'Could not retrieve data from Spirent')
            sys.exit(111)

        log.debug(f'Spirent test run={test_run_id} test results received successfully')

        test_results = response.json()
        log.debug(f'Spirent test run result is {test_results}')
        return test_results

    # def copy_test_outpus_from_spirent(self, test_run_id):
    #     log.info('......')
    #     self.spirent_report_path = BuiltIn().get_variable_value("${DEFAULT_TEST_LOGS_PATH}")
    #     tr_spirent_pcap_path = os.path.join(env_data_obj.output_path, each_test_id, "spirent_pcap_files")
    #     self.spirent_report_path=tr_spirent_pcap_path
    #     if test_run_id:
    #         if not os.path.exists(self.spirent_report_path):
    #             log.info(
    #                 f'Spirent report path={self.spirent_report_path} not found. Create..')
    #             Path(self.spirent_report_path).mkdir(
    #                 parents=True, exist_ok=True, mode=0o755)

    #         for eachURL in self.spirent_report_urls:
    #             try:
    #                 subprocess.call("wget " + eachURL + " -P " +
    #                                 self.spirent_report_path, shell=True)
    #                 log.info(f'Spirent report={eachURL} received')
    #             except Exception as e:
    #                 log.info(f'Spirent report={eachURL} not received. Error={e}')

        # SpirentOperations().delete_test_run_mngr(self.test_run_id)

    def delete_test_run_mngr(self, test_run_id):
        return self.delete_test_run(test_run_id)

    def get_spirent_test_servers(self):
        """Spirent test sunucuları dizisi döner."""
        response = self.get_test_servers()
        if response.status_code != 200:
            log.error(f"Failed to retrieve test servers. Status code: {response.status_code}")
            sys.exit(102)

        return response.json().get('testServers')

    def get_test_server_or_exit(self, test_server_name):
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
        servers = self.get_spirent_test_servers()
        log.debug(f'Test Sunucuları için Spirent cevabı: {servers}')

        for s in servers:
            log.debug(f'Test Sunucusu: {s}')
            if s.get('name') == test_server_name:
                return s

        log.error(f"Test server with name '{test_server_name}' not found.")
        sys.exit(103)
