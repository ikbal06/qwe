import json
from resources.globalProperties import *
from resources.common.CommonOperations import *


class TestConfigOperations:

    def __init__(self, test_name=None, ts_name=None):
        self.test_name = test_name
        self.ts_name = ts_name
        self.parsed_config_file = read_json_file(CONFIG_FILE_PATH)

    def get_test_params(self):
        """Get test params that is in the cfg.json file.
           Test params are used to update spirent test session.
           According to test params, related test session is updated.
            Ex:  {
           "test_id": "KT_CN_010",
           "ue_ip4": "172.30.0.63",
           "perm_key": "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
           "op_key": "00000000000000000000000000000000",
           "msin": "001000063",
           "test_duration": 20
            }
        """

        if self.parsed_config_file.get('testParameters'):
            test_param_list = self.parsed_config_file.get('testParameters')
            for each_test_param in test_param_list:
                if self.test_name == each_test_param.get('test_id'):
                    return each_test_param
        else:
            log.warning('Test Bilgilerine erişemeyi bekliyordum ama boş geldi!')
            return None
        return None

    def get_spirent_ts_params(self):
        """Get spirent ts params that is in the cfg.json file.
          Spirent ts params are used to update spirent test session.
          According to spirent ts params, related test session is updated.

          Ex:    {
         "ts_name": "vts-VTO2",
         "spirent_gnb_ip": "10.10.20.230",
         "spirent_dn_ip": "10.10.22.240",
         "spirent_dn_interface": "eth2",
         "spirent_gnb_interface": "eth4"
          }
        """
        if self.parsed_config_file.get('tsParameters'):

            for each_spirent_ts_param in self.parsed_config_file['tsParameters']:
                if self.ts_name == each_spirent_ts_param.get('ts_name'):
                    return each_spirent_ts_param
        else:

            log.warning('TS Bilgilerine erişemeyi bekliyordum ama boş geldi!')
            return None
        return None
