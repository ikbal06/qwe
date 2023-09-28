import os
import sys
import json
import time
from datetime import datetime
from globalProperties import *
from spirent.SpirentOperations import *
from analizci.AnalizciClient import *
from EnvDataOperations import *
from common.CommonOperations import *
from ansible.AnsibleOperations import *
from TestConfigOperations import *


def main():

    env_data_obj = EnvDataOperations()
    print("env_var: ", env_data_obj)
    spirent_client = SpirentOperations()
    AnsibleOperations(env_data_obj.ansible_verbose,
                      env_data_obj.allinone_ip,
                      env_data_obj.mongodb_deployment_type,
                      env_data_obj.postgre_deployment_type,
                      env_data_obj.cn_deployment_type,
                      env_data_obj.k8s_namespace,
                      SSH_COPY_ID_PLAYBOOK_PATH,
                      ansible_user=env_data_obj.username
                      ).run_playbook()

    if env_data_obj.get_version == "enable":
        version_file_path = os.path.join(env_data_obj.output_path, "version.txt")
        os.environ["DEFAULT_VERSION_PATH"] = version_file_path
        AnsibleOperations(env_data_obj.ansible_verbose,
                          env_data_obj.allinone_ip,
                          env_data_obj.mongodb_deployment_type,
                          env_data_obj.postgre_deployment_type,
                          env_data_obj.cn_deployment_type,
                          env_data_obj.k8s_namespace,
                          GET_VERSION_PLAYBOOK_PATH,
                          version_file_path=version_file_path,
                          ansible_user=env_data_obj.username
                          ).run_playbook()

    if env_data_obj.run_test == "enable":

        check_connection(SPIRENT_IP, SPIRENT_PORT)
        spirent_client.check_test_server(env_data_obj.spirent_ts_name)
        for each_test_id in env_data_obj.test_ids:

            test_date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            tr_spirent_pcap_path = os.path.join(env_data_obj.output_path, each_test_id, "spirent_pcap_files")
            tr_robot_report_path = os.path.join(env_data_obj.output_path, each_test_id, "robot_report_files")
            tr_nf_pcap_path = os.path.join(env_data_obj.output_path, each_test_id, "nf_pcap_files")
            TEST_PLAYBOOK_PATH = os.path.join(PLAYBOOKS_PATH, each_test_id + '.yml')
            test_param = TestConfigOperations(test_name=each_test_id).get_test_params()

            if os.path.exists(TEST_PLAYBOOK_PATH):

                print("[OK] {} playbook exist.".format(each_test_id))

                if env_data_obj.get_pcap == "enable":

                    allinone_ip = env_data_obj.allinone_ip
                    pcap_name = f"{allinone_ip}_{test_date}.pcap"
                    print("[OK] Pcap capture start!!!")
                    AnsibleOperations(env_data_obj.ansible_verbose,
                                      env_data_obj.allinone_ip,
                                      env_data_obj.mongodb_deployment_type,
                                      env_data_obj.postgre_deployment_type,
                                      env_data_obj.cn_deployment_type,
                                      env_data_obj.k8s_namespace,
                                      START_TCPDUMP_PLAYBOOK_PATH,
                                      ansible_user=env_data_obj.username,
                                      pcap_name=pcap_name
                                      ).run_playbook()
                    print("[OK] Spirent test={} run operation start!!!".format(each_test_id))
                    AnsibleOperations(env_data_obj.ansible_verbose,
                                      env_data_obj.allinone_ip,
                                      env_data_obj.mongodb_deployment_type,
                                      env_data_obj.postgre_deployment_type,
                                      env_data_obj.cn_deployment_type,
                                      env_data_obj.k8s_namespace,
                                      TEST_PLAYBOOK_PATH,
                                      ansible_user=env_data_obj.username,
                                      h_mcc=env_data_obj.h_mcc,
                                      h_mnc=env_data_obj.h_mnc,
                                      ue_id=env_data_obj.h_mcc + env_data_obj.h_mnc + test_param['msin'],
                                      perm_key=test_param['perm_key'],
                                      ue_ip4=test_param['ue_ip4'],
                                      test_duration=env_data_obj.test_duration,
                                      spirent_pcap_files_path=tr_spirent_pcap_path,
                                      robot_files_path=tr_robot_report_path
                                      ).run_playbook()
                    print("[OK] Pcap fetch start!!!")
                    AnsibleOperations(env_data_obj.ansible_verbose,
                                      env_data_obj.allinone_ip,
                                      env_data_obj.mongodb_deployment_type,
                                      env_data_obj.postgre_deployment_type,
                                      env_data_obj.cn_deployment_type,
                                      env_data_obj.k8s_namespace,
                                      FETCH_PCAP_FILES_PATH,
                                      ansible_user=env_data_obj.username,
                                      nf_pcap_files_path=tr_nf_pcap_path,
                                      pcap_name=pcap_name
                                      ).run_playbook()

                    test_status = os.getenv(each_test_id)

                    check_connection(env_data_obj.analizci_ip, int(env_data_obj.analizci_port))
                    analizci_pcapname_wgz = os.path.join(tr_nf_pcap_path, pcap_name+".gz")
                    analizci_pcapname_wogz = os.path.join(tr_nf_pcap_path, pcap_name)
                    analizci_config_obj = AnalizciClient(env_data_obj.analizci_ip,
                                                         env_data_obj.analizci_port,
                                                         core_ip=env_data_obj.allinone_ip,
                                                         pcap_name_wgz=analizci_pcapname_wgz,
                                                         pcap_name_wogz=analizci_pcapname_wogz,
                                                         test_id=each_test_id
                                                         )
                    merged_pcapname = analizci_config_obj.upload_pcap()
                    if merged_pcapname:
                        analizci_config_obj.run_analyze(merged_pcapname)
                    else:
                        print("[NOK] Analizci run test fail!!!!")

            else:
                print("[NOK]{}Test playbook is not ready!! Tester should prepare it!!!".format(each_test_id))
    else:
        print("[OK] No need to run spirent test!!")

        if env_data_obj.get_pcap == "enable":
            test_date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            allinone_ip = env_data_obj.allinone_ip
            tr_nf_output_path = os.path.join(env_data_obj.output_path,  "nf_pcap_files")
            pcap_name = f"{allinone_ip}_{test_date}.pcap"
            AnsibleOperations(env_data_obj.ansible_verbose,
                              env_data_obj.allinone_ip,
                              env_data_obj.mongodb_deployment_type,
                              env_data_obj.postgre_deployment_type,
                              env_data_obj.cn_deployment_type,
                              env_data_obj.k8s_namespace,
                              START_TCPDUMP_PLAYBOOK_PATH,
                              ansible_user=env_data_obj.username,
                              pcap_name=pcap_name
                              ).run_playbook()
            time.sleep(env_data_obj.test_duration)
            AnsibleOperations(env_data_obj.ansible_verbose,
                              env_data_obj.allinone_ip,
                              env_data_obj.mongodb_deployment_type,
                              env_data_obj.postgre_deployment_type,
                              env_data_obj.cn_deployment_type,
                              env_data_obj.k8s_namespace,
                              FETCH_PCAP_FILES_PATH,
                              ansible_user=env_data_obj.username,
                              nf_pcap_files_path=tr_nf_pcap_path,
                              pcap_name=pcap_name
                              ).run_playbook()

    if env_data_obj.get_log == "enable":
        tr_log_path = os.path.join(env_data_obj.output_path, "logs")
        AnsibleOperations(env_data_obj.ansible_verbose,
                          env_data_obj.allinone_ip,
                          env_data_obj.mongodb_deployment_type,
                          env_data_obj.postgre_deployment_type,
                          env_data_obj.cn_deployment_type,
                          env_data_obj.k8s_namespace,
                          FETCH_LOG_FILES_PATH,
                          ansible_user=env_data_obj.username,
                          log_path=tr_log_path
                          ).run_playbook()
    else:
        print("[OK] No need to get log files!!")


if __name__ == '__main__':
    main()
