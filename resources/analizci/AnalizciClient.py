from resources.globalProperties import *
from resources.common.HttpClient import HttpClient
import json
from urllib.parse import urlparse, urlunparse
import jinja2
from resources.common.CommonOperations import *
import requests
from datetime import datetime as dt
import subprocess
from datetime import datetime
from robot.libraries.BuiltIn import BuiltIn
from resources.common.Logger import log


class AnalizciClient():

    # def __init__(self, analizci_url, **kwargs):
    def __init__(self, analizci_url, pcap_name, test_id):

        # super().__init__(
        #     analizci_url,
        #     # analizci_port,
        #     api_path=ANALIZCI_API_PATH
        # )
        # analizci_ip yerine analizci-_url geldi
        # süperde tanımlanan http de kullanılıyor. bunu içeri taşımak için yapmalıyız(kendi initimize)
        self.analizci_url = analizci_url
        self.test_id = test_id
        self.pcap_name = pcap_name
        # self.__dict__.update(kwargs)
        # self.create_alias_config()

    def create_alias_config(self):
        """It is used to create analizci test run data  dynamically.
           There is a template (jinja) which is named nfServices in the ./Resources/globalProperties.py
           This template is used to create analizci test run data dynamically. According to the changing needs, analizci test run data
            is created easily using below parameters.
        """
        environment = jinja2.Environment()
        template = environment.from_string(nfServices)
        updated_nf_services_content = template.render(
            allinone_ip=self.core_ip
        )
        nf_services = json.loads(updated_nf_services_content)  # json
        aliasJson = {
            "aliasGroupName": self.pcap_name_wogz + "_AliasGroup",
            "NFs": []
        }

        # Add NFs and their endpoints to the alias JSON
        for nfName in NFList:
            aliasJson["NFs"].append({
                "NFName": nfName,
                "endpoints": []
            })

        for nf in nf_services:
            for nfName in NFList:
                if nfName.lower() in nf["description"].lower():
                    aliasJson["NFs"][NFList.index(nfName)]["endpoints"].append({
                        "ip": self.core_ip,  # all in one ip in ens5
                        "port": nf["port"],
                        "portAlias": nf["portAlias"],
                        "description": nf["description"]
                    })

        self.created_alias_config = aliasJson

    def upload_pcap(self):

        # Specify the file to upload
        pcap_file = [('file', open(self.pcap_name, 'rb'))]
        # Send POST request to upload the file
        response = requests.post(self.analizci_url+'upload', data={"filename": "merged"}, files=pcap_file)
        json_response = response.json()
        print(response)
        if "filename" not in response.json():
            print("Pcap upload failed !! {}  didn't run on Analizci".format(self.test_id))
        else:
            return json_response["filename"]

    def run_analyze(self, merged_pcap):
        schema_name = dt.now().strftime('%d%m%y_%H%M%S')+"-"+self.test_id
        json_data_forRun = dict()
        json_data_forRun.update({'pcapName': merged_pcap})
        json_data_forRun.update({'testIds': [self.test_id]})
        json_data_forRun.update({'schemaName': schema_name})
        json_data_forRun.update({'mergedPcapName': schema_name})
        json_data_forRun.update({'emails': ['ikbal.kirklar@ulakhaberlesme.com.tr']})

        #     uploadedAliases: GlobalAlias;
        #     filter: string;
        #     decodes: Array<{ type: string; decode: string }>;
        #     _3gppVersion: string;
        #     schemaName: string;  senaryo ismi
        #     pcapName: string;
        #     mergedPcapName: string;
        #     testIds: string[];
        #     pcapId: string;
        #     emails?: string[]; array  # soru işareti varsa karşısı boş olabilir
        #     taskId?: string;
        #     groupId?: string; #redmine için
        #     testNames?: string[]; #ismin ux-zun olur kalsın id den koşmak daha iyi bazısında sembol var

        # json_data_forRun.update({'uploadedAliases': self.created_alias_config})
        headers = {'Content-Type': 'application/json'}
        json_reponse = requests.post(self.analizci_url, json=json_data_forRun, headers=headers)
        print(json_reponse.json())

    def analizciye_gonder(self):

        selectected_test_id = str(self.testId).replace(" ", "_")

        fullPath = "/tmp/test_outputs/"+selectected_test_id+"/nf_pcap_files/"
        print("/tmp/test_outputs/"+selectected_test_id+"/nf_pcap_files/")
        for gzFile in os.listdir(fullPath):
            if gzFile.endswith(".gz"):
                subprocess.check_output("gunzip "+fullPath+gzFile, shell=True, text=True)
        pcapList = []
        for pcapFile in os.listdir(fullPath):
            if pcapFile.endswith(".pcap"):
                pcapList.append(pcapFile.split("_")[1].split(".")[0])

        # Convert strings to datetime objects
        date_objects = [datetime.strptime(date, '%d-%m-%Y-%H-%M-%S') for date in pcapList]
        # Find the latest date
        latest_pcap = max(date_objects)
        # Convert it back to a string
        latest_date_pcap = latest_pcap.strftime('%d-%m-%Y-%H-%M-%S')

        for pcapFile in os.listdir(fullPath):
            if pcapFile.endswith(".pcap"):
                if latest_date_pcap in pcapFile:
                    print(fullPath+pcapFile)
                    analizci_config_obj = AnalizciClient(
                        "http://analizci-test-back.ulakhaberlesme.com.tr/automated/", pcap_name=fullPath +
                        pcapFile, test_id=selectected_test_id)
                    merged_pcapname = analizci_config_obj.upload_pcap()
                    if merged_pcapname:
                        analizci_config_obj.run_analyze(merged_pcapname)
                        log.debug('başarısız olan test sonucu analizciye gönderildi')
                    else:
                        print("[NOK] Analizci run test fail!!!!")
                    break

    def analizciye_gonderme_secenegi(self, name):

        import json

        # JSON dosyasının yolunu belirtin
        json_dosya_yolu = '/workspace/.vscode/launch.json'

        # JSON dosyasını açın ve içeriği yükleyin
        with open(json_dosya_yolu, 'r') as dosya:
            veri = json.load(dosya)

        # "analizciye_gonderme_durumu" değerini alın
        analizciye_gonderme_durumu = veri["configurations"][4]["env"]["analizciye_gonderme_durumu"]

        # Elde edilen değeri yazdırın
        log.debug(analizciye_gonderme_durumu)

        test_status_return = BuiltIn().get_variable_value('${test_status}')
        test_status = test_status_return['criteriaStatus']

        if analizciye_gonderme_durumu == "1":
            log.debug("Case 1 seçildi. Böylece sadece başarısız olan testler analizciye gönderilecek.")
            if test_status == 'FAILED':
                log.debug(f'{self.testId}: testin bazı adımlarında veya tüm adımlarında hata var.')
                if name == self.testId:
                    AnalizciClient.analizciye_gonder(self)
            else:
                log.debug("Test başarılı olduğundan analizciye gönderilmedi")

        elif analizciye_gonderme_durumu == "2":
            log.debug("Case 2 seçildi. Böylece sadece başarılı olan testler analizciye gönderilecek.")
            if test_status == 'PASSED':
                log.debug(f'{self.testId}: test başarılı.')
                if name == self.testId:
                    AnalizciClient.analizciye_gonder(self)
            else:
                log.debug("Test başarısız olduğundan analizciye gönderilmedi.")

        elif analizciye_gonderme_durumu == "3":
            log.debug("Case 3 seçildi. Böylece tüm testler analizciye gönderilecek.")
            if name == self.testId:
                AnalizciClient.analizciye_gonder(self)
                log.debug(f"{self.testId} testi analizciye gönderildi.")
        else:
            log.warning("Geçersiz seçim. Lütfen 1, 2 veya 3 ten birini seçmiş olun.")

        return analizciye_gonderme_durumu
