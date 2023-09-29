import datetime
import json
import jinja2
import sys
import ansible_runner
from EnvDataOperations import EnvDataOperations
from ansible.AnsibleOperations import AnsibleOperations
from common.Logger import log
from globalProperties import *
from common.CommonOperations import *


env_data_obj = EnvDataOperations()

class AnsibleManager:

    def __init__(self, ansible_verbose, allinone_ip, mongodb_deployment_type, postgre_deployment_type,
                 cn_deployment_type, k8s_namespace, playbook_path, **kwargs):

        self.__dict__.update(kwargs)
        self.ansible_verbose = ansible_verbose
        self.allinone_ip = allinone_ip
        self.mongodb_deployment_type = mongodb_deployment_type
        self.postgre_deployment_type = postgre_deployment_type
        self.cn_deployment_type = cn_deployment_type
        self.k8s_namespace = k8s_namespace

        self.playbook_path = playbook_path
        self.extra_vars = kwargs
        self.create_dynamic_inventory()
        print(self.extra_vars)

    def create_dynamic_inventory(self):
        """It is used to create ansible inventory file dynamically.
         There is a template (jinja) which is named inventory_template in the ./Resources/globalProperties.py
         This template is used to create ansible inventory file dynamically. According to the changing needs, ansible inventory file
          is created easily using below parameters.
        """
        environment = jinja2.Environment()
        template = environment.from_string(inventory_template)

        update_content = template.render(
            allinone_ip=self.allinone_ip,
            mongodb_deployment_type=self.mongodb_deployment_type,
            postgre_deployment_type=self.postgre_deployment_type,
            cn_deployment_type=self.cn_deployment_type,
            k8s_namespace=self.k8s_namespace
        )
        print(update_content)
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
        print(f"Ansible Command:{ansible_commad}")
        result = ansible_runner.run(**ansible_commad)
        if result.stats.get('failures'):
            msg = f"{self.playbook_path} playbook failed!!!"
            log.error(msg)
            sys.exit(msg)

# --------------------------------------------------------

    def get_installed_packages_and_versions():
        version_file_path = os.path.join(env_data_obj.output_path, "version.txt")
        os.environ["DEFAULT_VERSION_PATH"] = version_file_path
        ansible = AnsibleManager(env_data_obj.ansible_verbose,
                          env_data_obj.allinone_ip,
                          env_data_obj.mongodb_deployment_type,
                          env_data_obj.postgre_deployment_type,
                          env_data_obj.cn_deployment_type,
                          env_data_obj.k8s_namespace,
                          GET_VERSION_PLAYBOOK_PATH,
                          version_file_path=version_file_path,
                          ansible_user=env_data_obj.username
                          )
        ansible.run_playbook()
        
    def copy_ssh_id_to_servers():
        print("env_var: ", env_data_obj)
        ansible = AnsibleManager(env_data_obj.ansible_verbose,
                        env_data_obj.allinone_ip,
                        env_data_obj.mongodb_deployment_type,
                        env_data_obj.postgre_deployment_type,
                        env_data_obj.cn_deployment_type,
                        env_data_obj.k8s_namespace,
                        SSH_COPY_ID_PLAYBOOK_PATH,
                        ansible_user=env_data_obj.username
                        )
        ansible.run_playbook()
        
    def start_packet_capture():
        test_date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        allinone_ip = env_data_obj.allinone_ip
        pcap_name = f"{allinone_ip}_{test_date}.pcap"
        print("[OK] Pcap capture start!!!")
        ansible = AnsibleManager(env_data_obj.ansible_verbose,
                            env_data_obj.allinone_ip,
                            env_data_obj.mongodb_deployment_type,
                            env_data_obj.postgre_deployment_type,
                            env_data_obj.cn_deployment_type,
                            env_data_obj.k8s_namespace,
                            START_TCPDUMP_PLAYBOOK_PATH,
                            ansible_user=env_data_obj.username,
                            pcap_name=pcap_name
                            )
        ansible.run_playbook()

    def fetch_pcap_files(_test_id):
        print("[OK] Pcap fetch start!!!")
        test_date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        allinone_ip = env_data_obj.allinone_ip
        pcap_name = f"{allinone_ip}_{test_date}.pcap"
        tr_nf_pcap_path = os.path.join(env_data_obj.output_path, _test_id, "nf_pcap_files")
        ansible = AnsibleManager(env_data_obj.ansible_verbose,
                            env_data_obj.allinone_ip,
                            env_data_obj.mongodb_deployment_type,
                            env_data_obj.postgre_deployment_type,
                            env_data_obj.cn_deployment_type,
                            env_data_obj.k8s_namespace,
                            FETCH_PCAP_FILES_PATH,
                            ansible_user=env_data_obj.username,
                            nf_pcap_files_path=tr_nf_pcap_path,
                            pcap_name=pcap_name
                            )
        ansible.run_playbook()