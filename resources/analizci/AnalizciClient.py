from resources.globalProperties import *
from resources.common.HttpClient import HttpClient
import json
from urllib.parse import urlparse, urlunparse
import jinja2
from resources.common.CommonOperations import *


class AnalizciClient(HttpClient):

    def __init__(self, analizci_ip, analizci_port, **kwargs):

        super().__init__(
            analizci_ip,
            analizci_port,
            api_path=ANALIZCI_API_PATH
        )

        self.__dict__.update(kwargs)
        unzip_file(self.pcap_name_wgz, self.pcap_name_wogz)
        self.create_alias_config()

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
        pcap_file = [('file', open(self.pcap_name_wogz, 'rb'))]
        # Send POST request to upload the file
        response = self.post(path='upload', data={"filename": "merged"}, files=pcap_file)
        json_response = response.json()
        if "filename" not in response.json():
            print("Pcap upload failed !! {}  didn't run on Analizci".format(self.test_id))
        else:
            return json_response["filename"]

    def run_analyze(self, merged_pcap):

        json_data_forRun = dict()
        json_data_forRun.update({'pcapName': merged_pcap})
        json_data_forRun.update({'testIds': [self.test_id]})
        json_data_forRun.update({'uploadedAliases': self.created_alias_config})

        json_reponse = self.post(data=json_data_forRun)
        print(json_reponse.json())
