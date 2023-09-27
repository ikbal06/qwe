# Variables içindeki değişkenler: BÜYÜK HARF
# Keywords metotlarının Arguments: _degisken_adi
# Keywords metotlarının yerel değişkenleri: degisken_adi

*** Settings ***
Library    listeners/MyListener.py
Resource    keywords/spirent.robot
Library    String

*** Variables ***
# KIWI 
${KIWI_TEST_ID}    168
${KIWI_PLAN_ID}    7 
# SPIRENT
${SPIRENT_TEST_ID}    KT_CN_001
${SPIRENT_RUNNING_TEST_ID}    
${SPIRENT_SERVER_NAME}    vts-VTO2
${ALLINONE_IP}    192.168.13.71
${MONGODB_DEPLOYMENT_TYPE}    cnf
${K8S_NAMESPACE}    default
${POSTGRE_DEPLOYMENT_TYPE}    cnf
${CN_DEPLOYMENT_TYPE}    vnf
${N6_IP}    10.10.22.33
${UPF_IP}    ${N6_IP}
${PUBLIC_IP}    10.10.20.22
${AMF_IP}    ${PUBLIC_IP}
${H_MCC}    001
${H_MNC}    001

*** Test Cases ***
Periyodik Kayıtlanma Testi [KT_CN_002]
    [Documentation]    Kt_cn_002 testini çalşıtıracağız
    [Setup]    Prepare Setup
    ${result} =    Run Process    ansible-playbook    playbooks/KT_CN_002.yml    
    ${isSpirentReady}=    Is Spirent Ready    ${SPIRENT_SERVER_NAME}
    Should Be True    ${isSpirentReady} 
    ${SPIRENT_TEST_ID}=    Set Variable    KT_CN_002
    ${result} =    Update Test Session    _test_name=${SPIRENT_TEST_ID}    _h_mnc=${H_MNC}    _h_mcc=${H_MCC}    _amf_ip=${AMF_IP}    _upf_ip=${UPF_IP}
    Should Be True    ${result}
    ${SPIRENT_RUNNING_TEST_ID} =    Run Test    ${SPIRENT_TEST_ID}
    ${test_status}=    Check Status Until Test Is Completed    ${SPIRENT_RUNNING_TEST_ID}
    Should Be Equal As Strings    "${test_status['testStateOrStep']}"    "COMPLETE"
    Log    naber


*** Keywords ***
Prepare Setup
    [Documentation]    Ansible ile test ortamını hazırlayacağız
    # Set Environment Variable    RUNNING_TEST_ID    ${RUNNING_TEST_ID}
    # Set Environment Variable    ${SPIRENT_TEST_ID}    PASSED
    Set Global Variable    ${KIWI_PLAN_ID}
    Set Global Variable    ${KIWI_PLAN_ID}
    Set Global Variable    ${SPIRENT_TEST_ID}
    Set Global Variable    ${SPIRENT_SERVER_NAME}
    Set Global Variable    ${SPIRENT_RUNNING_TEST_ID}
    # ${result} =    Run Process    ansible-playbook    playbooks/KT_CN_001.yml