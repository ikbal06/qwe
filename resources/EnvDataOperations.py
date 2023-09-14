import os
import sys
from globalProperties import *

class EnvDataOperations:

     def __init__(self):
     
         self.h_mcc = os.getenv('h_mcc', DEFAULT_MCC)
         self.h_mnc = os.getenv('h_mnc', DEFAULT_MNC)
         self.test_duration = os.getenv('test_duration', DEFAULT_TD)
         self.cn_deployment_type = os.getenv('cn_deployment_type', DEFAULT_CN_DEP_TYPE)
         self.mongodb_deployment_type = os.getenv('mongodb_deployment_type', DEFAULT_MONGODB_DEP_TYPE)
         self.postgre_deployment_type = os.getenv('postgre_deployment_type', DEFAULT_POSTGRE_DEP_TYPE)
         self.k8s_namespace = os.getenv('k8s_namespace', DEFAULT_K8S_NAMESPACE)
         self.get_pcap = os.getenv('get_pcap', DEFAULT_GET_PCAP)
         self.get_log = os.getenv('get_log', DEFAULT_GET_LOG)
         self.get_version = os.getenv('get_version', DEFAULT_GET_VERSION)
         self.run_test = os.getenv('run_test', DEFAULT_RUN_TEST)
         #self.analizci_ip = os.getenv('analizci_host', DEFAULT_ANALIZCI_HOST).split(':')[0]
         #self.analizci_port = os.getenv('analizci_host', DEFAULT_ANALIZCI_HOST).split(':')[1]
         self.ansible_verbose = os.getenv('ansible_verbose', 1)
         self.spirent_ts_name = os.getenv('spirent_ts_name')
         #self.test_ids=["KT_CN_001"]
         self.test_ids = os.getenv('test_ids').split(',')
         self.output_path = os.getenv('output_path')
         self.username = os.getenv('username')
         self.password = os.getenv('password')
         self.allinone_ip = os.getenv('allinone_ip')
         self.public_ip = os.getenv('public_ip')
         self.n6_ip = os.getenv('n6_ip')
         self.env_data_validator()
     
     def env_data_validator(self):
     
             if not self.spirent_ts_name:
                sys.exit("[NOK] Missing spirent_ts_name information. Please give spirent_ts_name as environment variable") 
             if not self.test_ids:
                sys.exit("[NOK] Missing test_ids information. Please give test_ids as environment variable")   
             if not self.output_path:
                sys.exit("[NOK] Missing output_path information. Please give output_path as environment variable")
             if not self.username:
                sys.exit("[NOK] Missing username information. Please give username as environment variable")
             if not self.password:
                sys.exit("[NOK] Missing password information. Please give password as environment variable")
             if not self.allinone_ip:
                sys.exit("[NOK] Missing allinone_ip information. Please give allinone_ip as environment variable")             
             if not self.public_ip:
                sys.exit("[NOK] Missing public_ip information. Please give public_ip as environment variable") 
             if not self.n6_ip:
                sys.exit("[NOK] Missing n6_ip information. Please give n6_ip as environment variable") 


