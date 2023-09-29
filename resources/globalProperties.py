import os
import shutil
from common.CommonOperations import *

# Spirent properties
SPIRENT_IP = '192.168.13.99'
SPIRENT_PORT = 8080
SPIRENT_PROTOCOL = 'http'
SPIRENT_USER = 'automated'
SPIRENT_PASSWORD = 'a1b2c3d4'
SPIRENT_API_PATH = 'api/'

# DEFAULT_ANALIZCI_HOST = "10.10.10.10:3000".split(":")
# DEFAULT_ANALIZCI_IP = DEFAULT_ANALIZCI_HOST[0]
# DEFAULT_ANALIZCI_PORT = DEFAULT_ANALIZCI_HOST[1]
ANALIZCI_PROTOCOL = 'http'
ANALIZCI_API_PATH = 'automated/'

DEFAULT_TEST_SERVER = "vTS1"
DEFAULT_TEST_ENV = "vto"
DEFAULT_MCC = "001"
DEFAULT_MNC = "002"
DEFAULT_USERNAME = "ubuntu"
DEFAULT_PWD = " test123"
DEFAULT_TEST_RESULTS_PATH = "/etc/test_logs/"
DEFAULT_SUT_NAME = "automated_amf"
DEFAULT_TD = 120
DEFAULT_TEST_IDS = "KT_CN_001,KT_CN_002"
DEFAULT_GET_PCAP = "disable"
DEFAULT_GET_LOG = "disable"
DEFAULT_GET_VERSION = "disable"
DEFAULT_RUN_TEST = "enable"
DEFAULT_CN_DEP_TYPE = "vnf"
DEFAULT_MONGODB_DEP_TYPE = "cnf"
DEFAULT_POSTGRE_DEP_TYPE = "cnf"
DEFAULT_K8S_NAMESPACE = "default"


ANSIBLE_PLAYBOOK_PATH = shutil.which("ansible-playbook")
BASE_PATH = "/workspace"
CONFIG_FILE_PATH = os.path.join(BASE_PATH, "config.json")
PLAYBOOKS_PATH = os.path.join(BASE_PATH, "playbooks")  # BASE_PATH//playbooks
ROLES_PATH = os.path.join(BASE_PATH, "roles")  # BASE_PATH//roles
SSH_COPY_ID_PLAYBOOK_PATH = os.path.join(PLAYBOOKS_PATH, "ULAK5G_core_ssh_copy_id.yml")
START_TCPDUMP_PLAYBOOK_PATH = os.path.join(PLAYBOOKS_PATH, "ULAK5G_core_start_tcpdump.yml")
print(START_TCPDUMP_PLAYBOOK_PATH)
GET_VERSION_PLAYBOOK_PATH = os.path.join(PLAYBOOKS_PATH, "ULAK5G_core_get_nf_version.yml")
FETCH_PCAP_FILES_PATH = os.path.join(PLAYBOOKS_PATH, "ULAK5G_core_fetch_pcap_files.yml")
FETCH_LOG_FILES_PATH = os.path.join(PLAYBOOKS_PATH, "ULAK5G_core_fetch_log_files.yml")
# BASE_PATH//roles, BASE_PATH//playbooks//roles
# create_symlink(ROLES_PATH, os.path.join(PLAYBOOKS_PATH, "roles"))


inventory_template = """{
   "vars":{    
      "mongo_db_username":"cnrusr",
      "mongo_db_password":"P5vKG6vE",
      "mongo_db_port":27017,
      "postgre_db_username":"cnrusr",
      "postgre_db_password":"P5vKG6vE",
      "postgre_db_port":5432,
      "postgre_db_name":"newstodb",
      "ansible_become":"true"
   },
   "hosts":{
     "allinone":{
         "ansible_host":"{{allinone_ip}}"
      },
      "mongo":{
         "ansible_host":"{{allinone_ip}}"
      },
      "postgre":{
         "ansible_host":"{{allinone_ip}}"
      }
   },
    "children":{

      "mongodb":{
         "hosts":{
            "mongo":{
             "deployment_type":"{{mongodb_deployment_type}}",
             "container_name":"mongodb",
             "k8s_namespace":"{{k8s_namespace}}"

            }
         }
      },
      "postgredb":{
         "hosts":{
            "postgre":{
             "deployment_type":"{{postgre_deployment_type}}",
             "container_name":"pgdb",
             "k8s_namespace":"{{k8s_namespace}}"
            }
         }
      },
     "nfs":{
         "hosts":{
            "allinone":{  
            "deployment_type":"{{cn_deployment_type}}"  ,
            "k8s_namespace":"{{k8s_namespace}}"          
            }
         },
         "vars":{

            "log_files":[
                           {
                  "path":"/var/log/cinar/amf"
               },
               {
                  "path":"/var/log/cinar/pcf/cs"
               },
               {
                  "path":"/var/log/cinar/pcf/ams"
               },
               {
                  "path":"/var/log/cinar/pcf/sms"
               },
               {
                  "path":"/var/log/cinar/pcf/pes"
               },
               {
                  "path":"/var/log/cinar/pcf/nfrs"
               },
               {
                  "path":"/var/log/cinar/ausf"
               },
               {
                  "path":"/var/log/cinar/udm"
               },
               {
                  "path":"/var/log/cinar/udr"
               },
               {
                  "path":"/var/log/cinar/nrf"
               },
               {
                  "path":"/var/log/cinar/nssf"
               },

               {
                  "path":"/var/log/cinar/smf"
               },
               {
                  "path":"/var/log/cinar/upf"
               }
            ],
            "package_names":[
               "cnr"               
            ]
         }  
         }  
         }     
}"""


# List of NFs
NFList = [
    "NRF",
    "NEF",
    "PCF",
    "NSSF",
    "AMF",
    "UDM",
    "AUSF",
    "UDR",
    "SMF"  # add more NFs here
]

# List of NRF services
nfServices = """[
            {
                "ip": "{{allinone_ip}}",
                "port": "8001",
                "portAlias": "",
                "description": "nrfName"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "8006",
                "portAlias": "",
                "description": "nrfName"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "8007",
                "portAlias": "",
                "description": "nrfName"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "7000",
                "portAlias": "",
                "description": "pcf"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "7008",
                "portAlias": "",
                "description": "pcf"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "7002",
                "portAlias": "",
                "description": "pcf"
            },
            
            {
                "ip": "{{allinone_ip}}",
                "port": "7050",
                "portAlias": "",
                "description": "pcf"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "7052",
                "portAlias": "",
                "description": "pcf"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "7052",
                "portAlias": "",
                "description": "pcf"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "5001",
                "portAlias": "",
                "description": "udm"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "5002",
                "portAlias": "",
                "description": "udm"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "5003",
                "portAlias": "",
                "description": "udm"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "5004",
                "portAlias": "",
                "description": "udm"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "5005",
                "portAlias": "",
                "description": "udm"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "5500",
                "portAlias": "",
                "description": "ausf"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "5400",
                "portAlias": "",
                "description": "udr"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "6210",
                "portAlias": "",
                "description": "amf"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "6211",
                "portAlias": "",
                "description": "amf"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "6310",
                "portAlias": "",
                "description": "smsf"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "6110",
                "portAlias": "",
                "description": "smf"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "6123",
                "portAlias": "",
                "description": "smf"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "",
                "portAlias": "",
                "description": "amfName"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "6110",
                "portAlias": "",
                "description": "smfName"
            },
            {
                "ip": "{{allinone_ip}}",
                "port": "",
                "portAlias": "",
                "description": "amfName"
            }
        ]
"""

test_Session_template = """{
	"library": "{{ lib_id }}",
	"name": "{{ test_id }}",
	"steps": [{
			"delaySec": 0,
			"predecessorState": "",
			"predecessorTcIndex": -1,
			"predecessorTsIndex": -1,
			"tcActivity": "Init",
			"tcIndex": 0,
			"tsIndex": 0
		},
		{
			"delaySec": 0,
			"predecessorState": "",
			"predecessorTcIndex": -1,
			"predecessorTsIndex": -1,
			"tcActivity": "Start",
			"tcIndex": 0,
			"tsIndex": 0
		},
		{
			"delaySec": "{{test_duration}}",
			"predecessorState": "",
			"predecessorTcIndex": -1,
			"predecessorTsIndex": -1,
			"tcActivity": "Stop",
			"tcIndex": 0,
			"tsIndex": 0
		},
		{
			"delaySec": 0,
			"predecessorState": "STOPPED",
			"predecessorTcIndex": 0,
			"predecessorTsIndex": 0,
			"tcActivity": "Cleanup",
			"tcIndex": 0,
			"tsIndex": 0
		}
	],
	"tsGroups": [{
		"tsId": "{{ ts_id }}",
		"testCases": [{
			"name": "",
			"type": "AMF Nodal",
			"associatedPhys": [],
			"parameters": {
				"ActiveEntryTimeMs": "0",
				"AmfSut": {
					"class": "Sut",
					"name": "{{ amf_info }}"
				},
				"GnbControlAddr": {
					"class": "TestNode",
					"ethStatsEnabled": false,
					"forcedEthInterface": "{{gnb_interface_info}}",
					"innerVlanId": 0,
					"ip": "{{ gnb_ip}}",
					"mac": "",
					"mtu": 1500,
					"nextHop": "",
					"numLinksOrNodes": 1,
					"numVlan": 1,
					"phy": "{{gnb_interface_info}}",
					"uniqueVlanAddr": false,
					"vlanDynamic": 0,
					"vlanId": 0,
					"vlanUserPriority": 0,
					"vlanTagType": 0
				},
				"GnbMcc": "{{ h_mcc }}",
				"GnbMnc": "{{ h_mnc }}",
                "UeNas5gMmSecretKey" : "0x{{perm_key}}",
                "UeNas5gMmOpVar": "0x{{op_key}}",	
				"NetworkHostAddrLocal": {
					"class": "TestNode",
					"ethStatsEnabled": false,
					"forcedEthInterface": "{{dn_interface_info}}",
					"innerVlanId": 0,
					"ip": "{{dn_ip}}",
					"mac": "",
					"mtu": 1500,
					"nextHop": "{{ n6_ip }}",
					"numLinksOrNodes": 1,
					"numVlan": 1,
					"phy": "{{dn_interface_info}}",
					"uniqueVlanAddr": false,
					"vlanDynamic": 0,
					"vlanId": 0,
					"vlanUserPriority": 0,
					"vlanTagType": 0
				},
				"UeNas5gMmSupi": "{{ ue_id }}",
                "UeNas5gMmMncLength": "{{ mnc_length }}"
			}
		}]
	}]
}"""

# Test Names
testDescriptions = {
    "KT_CN_001": "İlk Kayıtlanma/Kimlik Doğrulama",
    "KT_CN_002": "Periyodik Kayıtlanma",
    "KT_CN_003": "Hareketlilik Kayıtlanması",
    "KT_CN_004": "Servis Alanı Kısıtlamaları",
    "KT_CN_005": "Kullanıcı Ekipmanı İçerik Transferi-Kimlik Doğrulama - 3GPP TS 23.502 V15.6.0 4.2.2.2.2",
    "KT_CN_006": "AMF Yük Yeniden Dengeleme",
    "KT_CN_007": "AMF’in Slice Bilgisine Göre Direct Reroute Yöntemi ile Değiştirilmesi",
    "KT_CN_008": "UE Tarafından Başlatılan Kayıt Silme – 3GPP TS 23.502 V15.6.0 4.2.2.3.2",
    "KT_CN_009": "Ağ tarafından başlatılan kayıt silme",
    "KT_CN_010": "PDU Oturumu Kurulumu",
    "KT_CN_011": "LADN",
    "KT_CN_012": "Xn Handover UPF Değişimi Olmaksızın-UPF Endmarker",
    "KT_CN_019": "Süre Tabanlı Tamponlama",
    "KT_CN_020": "Paket Sayısı Tabanlı Tamponlama",
    "KT_CN_022": "UE Configuration Update",
    "KT_CN_023": "AN Release",
    "KT_CN_024": "AM Policy Association Modification initiated by the AMF",
    "KT_CN_026": "Procedures for future background data transfer",
    "KT_CN_027": "Usage Monitoring Control (kullanım izleme yönetimi) - PDU Session Level (Paket veri birimi oturumu seviyesinde) volume based (data hacmi bazlı)",
    "KT_CN_028": "Usage Monitoring Control (kullanım izleme yönetimi) - Pcc Rule/SDF Level (Servis seviyesinde) volume based (data hacmi bazlı)",
    "KT_CN_029": "Usage Monitoring Control (kullanım izleme yönetimi) - PDU Session Level (Paket veri birimi oturumu seviyesinde) duration based (zaman bazlı)",
    "KT_CN_032": "UE’ye ConfiguredNSSAI Bilgisinin İletimi",
    "KT_CN_033": "Requested NSSAI Limitasyonu",
    "KT_CN_035": "Farklı NSSAI bilgilerini bir ağ dilimiyle ilişkilendirme",
    "KT_CN_036": "Farklı Ağ Dilimlerini bir NSSAI ile ilişkilendirme",
    "KT_CN_040": "Parameter Provisioning",
    "KT_CN_042": "AF Kısıtlama",
    "KT_CN_043": "Monitoring Events (Location Reporting)",
    "KT_CN_044": "Monitoring Events (Loss of Connectivity)",
    "KT_CN_045": "Monitoring Events (UE Reachability for Data)",
    "KT_CN_049": "Servis İsteği",
    "KT_CN_050": "PDU Oturum sonlandırma-Kullanıcı Ekipmanı Tarafından Başlatılan",
    "KT_CN_051": "PDU Oturum sonlandırma-PCF Tarafından Başlatılan",
    "KT_CN_052": "AMF ve SMF Bilgilendirme",
    "KT_CN_053": "Xn Handover- UPF Değişimi olmaksızın",
    "KT_CN_054": "Xn Handover- I-UPF Eklenmesi",
    "KT_CN_056": "N2 Handover",
    "KT_CN_058": "Setting up an AF Session with Required QoS Procedure - AF Session Termination (PDU Session Release triggered)",
    "KT_CN_065": "Tıkanıklık kontolü General-Acil Durum Servisi",
    "KT_CN_068": "IMS - AF Session Termination (PDU Session Release triggered )",
    "KT_CN_070": "AF isteklerinde abonelik bilgisi uygunluğu kontrolü",
    "KT_CN_072": "IMS - Erişim şebeke bilgisi raporlama (AN_INFO report)",
    "KT_CN_074": "Yük Dengeleme",
    "KT_CN_079": "Tıkanıklık kontolü General - 3gpp TS 23.502 V15.6.0",
    "KT_CN_080": "Tıkanıklık kontolü DNN Tabanlı - 3gpp TS 23.502 V15.6.0",
    "KT_CN_081": "Tıkanıklık kontolü Slice Tabanlı - 3gpp TS 23.502 V15.6.0",
    "KT_CN_083": "PDU Session IMS - 3gpp TS 23.502 V15.6.0",
    "KT_CN_087": "Overload Paging- 3gpp TS 23.502 V15.6.0",
    "KT_CN_107": "5GCN/IMS Performans Metrikleri ve KPI’ların Gösterimi-N2 Handover",
    "KT_CN_108": "5GCN/IMS Performans Metrikleri ve KPI’ların Gösterimi-Acil Durum Kayıtlanması",
    "KT_CN_109": "5GCN/IMS Performans Metrikleri ve KPI’ların Gösterimi-PDU Session Fail",
    "KT_CN_110": "5GCN/IMS Performans Metrikleri ve KPI’ların Gösterimi-Periyodik Kayıtlanma",
    "KT_CN_111": "5GCN/IMS Performans Metrikleri ve KPI’ların Gösterimi-N2 Handover fail",
    "KT_CN_112": "5GCN/IMS Performans Metrikleri ve KPI’ların Gösterimi",
    "KT_IMS_002": "Registration over 5G",
    "KT_IMS_004": "VoNR",
    "KT_IMS_017": "Video over NR",
    "KT_IMS_203": "VoNR - SKT",
    "KT_IMS_204": "Video over NR",
    "KT_IMS_209": "SMS over 5G ",
    "5G_CN_SystemPerformanceScenario_5_1": "withoutIMS_L2_1200-pdu-data",
    "5G_CN_SystemPerformanceScenario_5_2": "withoutIMS_L2_4800_reg",
    "5G_CN_SystemPerformanceScenario_6": "2400-teknodal-IMS",
    "KT_EPC_001": "İlk Kayıtlanma/Kimlik Doğrulama",
    "KT_EPC_003": "Trackig Area Update",
    "KT_EPC_004": "Emergency Service",
    "KT_EPC_005": "Handover",
    "KT_EPC_011": "APN bazlı paket filtreleme",
    "KT_EPC_012": "Roaming",
    "KT_EPC_021": "IPv6 ile data trafiği"
}
