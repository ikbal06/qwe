import jinja2
import json
from globalProperties import *

def create_test_run_data(pcapname_in, each_test_id_in, allinone_ip_in):
    """It is used to create analizci test run data  dynamically.
        There is a template (jinja) which is named nfServices in the ./resources/globalProperties.py
        This template is used to create analizci test run data dynamically. According to the changing needs, analizci test run data
         is created easily using below parameters.
     """
    environment = jinja2.Environment()
    template = environment.from_string(nfServices)
    updated_nf_services_content = template.render(
        allinone_ip=allinone_ip_in
    )
    nf_services = json.loads(updated_nf_services_content)  # json
    aliasJson = {
        "aliasGroupName": pcapname_in + "_AliasGroup",
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
                    "ip": allinone_ip_in,  # all in one ip in ens5
                    "port": nf["port"],
                    "portAlias": nf["portAlias"],
                    "description": nf["description"]
                })

    return aliasJson
