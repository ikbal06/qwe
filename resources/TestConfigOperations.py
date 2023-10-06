import json
from resources.globalProperties import *
from resources.common.CommonOperations import *


class TestConfigOperations:
    """Test Parametrelerini ve Spirent Ayarlarını ./config.json dosyasından okuyarak kullanıma sunar.

    ```json

        "testParameters": [{
            "test_id": "KT_CN_001",
            "ue_ip4": "172.30.0.63",
            "perm_key": "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
            "op_key": "00000000000000000000000000000000",
            "msin": "001000063",
            "test_duration": 10
        }, ....

        "tsParameters": [
            {
            "ts_name": "vTS1",
            "spirent_gnb_ip": "10.10.20.230",
            "spirent_dn_ip": "10.10.22.240",
            "spirent_dn_interface": "eth5",
            "spirent_gnb_interface": "eth4"
        }, ....

        ]

    ```
    """

    def __init__(self, test_name=None, ts_name=None):
        log.debug(f"test_name:{test_name}  <>  ts_name:{ts_name}")
        self.test_name = test_name
        self.ts_name = ts_name
        # self.parsed_config_file = read_json_file(CONFIG_FILE_PATH)
        try:  # JSON dosyasını okuma modunda açalım
            log.debug(f"{CONFIG_FILE_PATH} JSON dosyasısı okunacak")
            with open(CONFIG_FILE_PATH, 'r') as json_file:
                self.parsed_config_file = json.load(json_file)
        except FileNotFoundError:  # dosya bulunamazsa
            log.error(f"JSON dosyası bulunamadı: {CONFIG_FILE_PATH}")
            sys.exit(222)
        except json.JSONDecodeError as e:  # JSON verisi geçersizse
            log.error(f"JSON dosyası okunamadı: {e}")
            sys.exit(222)
        except Exception as e:  # Diğer istisnalar
            log.error(f"Beklenmeyen bir hata oluştu: {e}")
            sys.exit(222)

    def get_test_params_by_test_name(self, _test_name):
        """Get test params that is in the cfg.json file.
           Test params are used to update spirent test session.
           According to test params, related test session is updated.

           ```json

            Ex:  {
           "test_id": "KT_CN_010",
           "ue_ip4": "172.30.0.63",
           "perm_key": "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
           "op_key": "00000000000000000000000000000000",
           "msin": "001000063",
           "test_duration": 20
            }
            ```
        """
        if self.parsed_config_file.get('testParameters'):
            test_param_list = self.parsed_config_file.get('testParameters')
            for each_test_param in test_param_list:
                if _test_name == each_test_param.get('test_id'):
                    return each_test_param
        else:
            log.warning('Test Bilgilerine erişemeyi bekliyordum ama boş geldi!')
            return None
        return None

    def get_test_params(self):
        """Get test params that is in the cfg.json file.
           Test params are used to update spirent test session.
           According to test params, related test session is updated.

           ```json

            Ex:  [{
           "test_id": "KT_CN_010",
           "ue_ip4": "172.30.0.63",
           "perm_key": "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
           "op_key": "00000000000000000000000000000000",
           "msin": "001000063",
           "test_duration": 20
            }, ... ]
            ```
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

    def _get_spirent_ts_params(self):
        """Get spirent ts params that is in the cfg.json file.
          Spirent ts params are used to update spirent test session.
          According to spirent ts params, related test session is updated.

        ```json 

          Ex:    [...{
         "ts_name": "vts-VTO2",
         "spirent_gnb_ip": "10.10.20.230",
         "spirent_dn_ip": "10.10.22.240",
         "spirent_dn_interface": "eth2",
         "spirent_gnb_interface": "eth4"
          }]
        ```
        """
        log.debug('Ayarlar dosyasında tsParameters bilgsi içindeki Spirent Sunucuları dönülecek')
        ts_params = self.parsed_config_file.get('tsParameters', [])
        if len(ts_params) == 0:
            log.error(f'Spirent sunucu bilgileri {CONFIG_FILE_PATH} dosyasında mevcut değil!')
            sys.exit(222)

        return ts_params

    def get_spirent_ts_params_by_test_name(self, _test_name):
        """Get spirent ts params that is in the cfg.json file.
          Spirent ts params are used to update spirent test session.
          According to spirent ts params, related test session is updated.

        ```json 

          Ex:    {
         "ts_name": "vts-VTO2",
         "spirent_gnb_ip": "10.10.20.230",
         "spirent_dn_ip": "10.10.22.240",
         "spirent_dn_interface": "eth2",
         "spirent_gnb_interface": "eth4"
          }
        ```
        """
        for ts in self._get_spirent_ts_params():
            log.debug(f"Spirent sunucu: {ts.get('ts_name')}")
            if ts.get('ts_name') == _test_name:
                return ts

        log.error(f'<{_test_name}> isimli TS sunucu {CONFIG_FILE_PATH} dosyasında tanımlı Spirent sunucu bilgileri arasında yok!')
        sys.exit(222)
