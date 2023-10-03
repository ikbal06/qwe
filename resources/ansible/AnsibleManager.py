from datetime import datetime
import json
import jinja2
import sys
import ansible_runner
import os
from robot.api.deco import keyword, not_keyword
from resources.TestConfigOperations import TestConfigOperations
from resources.EnvDataOperations import EnvDataOperations
from resources.common.Logger import log
from resources.globalProperties import *
from resources.common.CommonOperations import *

env_data_obj = EnvDataOperations()
log.debug(f"env_data_obj: {env_data_obj}")


class AnsibleManager:

    def __init__(self):
        self.ansible_verbose = env_data_obj.ansible_verbose
        self.allinone_ip = env_data_obj.allinone_ip
        self.mongodb_deployment_type = env_data_obj.mongodb_deployment_type
        self.postgre_deployment_type = env_data_obj.postgre_deployment_type
        self.cn_deployment_type = env_data_obj.cn_deployment_type
        self.k8s_namespace = env_data_obj.k8s_namespace
        self.extra_vars = {'ansible_user': env_data_obj.username}
        self.__dict__.update(self.extra_vars)
        self.create_dynamic_inventory()
        log.debug(f"AnsibleManager: {self}")

        test_date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        self.pcap_name = f"{self.allinone_ip}_{test_date}.pcap"
        dict_pcap_name = {"pcap_name": self.pcap_name}
        self.__dict__.update(dict_pcap_name)
        self.extra_vars.update(dict_pcap_name)

    def create_dynamic_inventory(self):
        """It is used to create ansible inventory file dynamically.
         There is a template (jinja) which is named inventory_template in the ./Resources/globalProperties.py
         This template is used to create ansible inventory file dynamically. According to the changing needs, ansible inventory file
          is created easily using below parameters.
        """
        template = jinja2.Environment().from_string(inventory_template)

        update_content = template.render(
            allinone_ip=self.allinone_ip,
            mongodb_deployment_type=self.mongodb_deployment_type,
            postgre_deployment_type=self.postgre_deployment_type,
            cn_deployment_type=self.cn_deployment_type,
            k8s_namespace=self.k8s_namespace
        )
        log.debug(update_content)
        hosts = json.loads(update_content)
        self.inventory = {'all': hosts}
        
    def run_playbook(self):
        """It is used to run ansible playbooks that is created in the ./playbooks
           Ansible_runner python library is used to run ansible playbooks programmaticaly.
        """
        ansible_commad = dict()
        ansible_commad.update({'extravars': self.extra_vars})
        ansible_commad.update({'playbook': self.playbook_path})
        ansible_commad.update({'inventory': self.inventory})
        ansible_commad.update({'verbosity': int(self.ansible_verbose)})
        log.debug(f"Ansible Command:{ansible_commad}")
        result = ansible_runner.run(**ansible_commad)
        if result.stats.get('failures'):
            msg = f"{self.playbook_path} playbook failed!!!"
            log.error(msg)
            sys.exit(msg)

        return result

    def run_test_playbook(self,test_id):
        print("[OK] Spirent test={} run operation start!!!".format(test_id))
        TEST_PLAYBOOK_PATH = os.path.join(PLAYBOOKS_PATH, test_id + '.yml')
        self.playbook_path = TEST_PLAYBOOK_PATH
        tr_spirent_pcap_path = os.path.join(env_data_obj.output_path, test_id, "spirent_pcap_files")
        tr_robot_report_path = os.path.join(env_data_obj.output_path, test_id, "robot_report_files")
        test_param = TestConfigOperations().get_test_params_by_test_name(test_id)
        dictim = {
            "h_mcc": env_data_obj.h_mcc,
            "h_mnc": env_data_obj.h_mnc,
            "ue_id": env_data_obj.h_mcc + env_data_obj.h_mnc + test_param['msin'],
            "perm_key": test_param['perm_key'],
            "ue_ip4": test_param['ue_ip4'],
            "test_duration": env_data_obj.test_duration,
            "spirent_pcap_files_path": tr_spirent_pcap_path,
            "robot_files_path": tr_robot_report_path
        }
        self.__dict__.update(dictim)
        self.extra_vars.update(dictim)
        return self.run_playbook()

    def copy_ssh_id_to_servers(self):
        self.playbook_path = SSH_COPY_ID_PLAYBOOK_PATH
        return self.run_playbook()

    def get_installed_packages_and_versions(self):
        self.playbook_path = GET_VERSION_PLAYBOOK_PATH
        version_file_path = os.path.join(env_data_obj.output_path, "version.txt")
        os.environ["DEFAULT_VERSION_PATH"] = version_file_path
        dictim = {"version_file_path": version_file_path}
        self.__dict__.update(dictim)
        self.extra_vars.update(dictim)
        return self.run_playbook()

    def start_packet_capture(self):
        self.playbook_path = START_TCPDUMP_PLAYBOOK_PATH
        log.debug("[OK] Pcap capture start!!!")
        return self.run_playbook()

    def fetch_pcap_files(self, _test_id):
        self.playbook_path = FETCH_PCAP_FILES_PATH
        dict_extra = {
            "nf_pcap_files_path": os.path.join(env_data_obj.output_path, _test_id, "nf_pcap_files"),
            "remote_tmp": "/tmp/ornek"
        }
        self.__dict__.update(dict_extra)
        self.extra_vars.update(dict_extra)
        log.debug("[OK] Pcap fetch start!!!")
        self.run_playbook()

