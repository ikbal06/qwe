import json
import jinja2
import sys
import ansible_runner
from common.Logger import log
from globalProperties import *
from common.CommonOperations import *


class AnsibleOperations:

    def __init__(self, ansible_verbose, allinone_ip, mongodb_deployment_type, postgre_deployment_type, cn_deployment_type, k8s_namespace, playbook_path, **kwargs):

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
        print("Ansible Command:{}".format(ansible_commad))
        result = ansible_runner.run(**ansible_commad)
        if result.stats.get('failures'):
            msg = f"{self.playbook_path} playbook failed!!!"
            log.error(msg)
            sys.exit(msg)
