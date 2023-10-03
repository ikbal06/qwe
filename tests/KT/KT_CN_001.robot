# Variables içindeki değişkenler: BÜYÜK HARF
# Keywords metotlarının Arguments: _degisken_adi
# Keywords metotlarının yerel değişkenleri: degisken_adi

*** Variables ***
# KIWI 
# Bu testin KIWI üstünde karşılığı olan Test Case ID bilgisi
# ${KIWI_TEST_ID}    168
# Bu testin SPIRENT üstünde koşturulacağı Spirent Test ID bilgisi 
${SPIRENT_TEST_ID}    KT_CN_001
${MONGODB_DEPLOYMENT_TYPE}    %{mongodb_deployment_type}
${K8S_NAMESPACE}    %{k8s_namespace}
${POSTGRE_DEPLOYMENT_TYPE}    %{postgre_deployment_type}
${CN_DEPLOYMENT_TYPE}    %{cn_deployment_type}
${H_MCC}    %{h_mcc}
${H_MNC}    %{h_mnc}

*** Settings ***
# Library    listeners/MyListener.py
Resource    keywords/spirent.robot  
# Library    capturer/pcapCapturer.py
Library    ansible.AnsibleManager
Library    String 
# Test Setup    Before Test
Test Teardown    After Test


*** Test Cases ***

BOŞ Kayıtlanma Testi [KT_CN_001]
    Log    Boş boş koş

Kayıtlanma Testi [KT_CN_001]
    [Documentation]    Çalıştırılacak testin adı ve ID değeri "KT_CN_001" olacak.
    ...    Çalışacağı Spirent test sunucusu parametre olarak gelebilir 
    ...    Önce Spirent sunucuları arasından arana spirent sunucusu bulunur (yoksa çıkılır -FAIL-)
    ...    Test Oturum Bilgisi Spirent üzerinde güncellenir
    ...    Spirent kullanıcı adı ve koşulacak testin ID bilgisi Spirent üstünde güncellenir
    [Tags]    ansible    BT CN 001
    # [Setup]    Prepare Setup
    ${isSpirentReady}=    Is Spirent Ready    ${SPIRENT_SERVER_NAME}
    Should Be True    ${isSpirentReady} 
    ${result}=    Update Test Session    _spirent_server_name=${SPIRENT_SERVER_NAME}    _test_name=${SPIRENT_TEST_ID}    _h_mnc=${H_MNC}    _h_mcc=${H_MCC}    _amf_ip=${AMF_IP}    _upf_ip=${UPF_IP}
    Should Be True    ${result}
    ${spirent_running_test_id}=    Run Test    ${SPIRENT_TEST_ID}
    ${test_status}=    Check Status Until Test Is Completed    ${spirent_running_test_id}
    Should Be Equal As Strings    "${test_status['testStateOrStep']}"    "COMPLETE"
    Copy Test Result Files From Spirent    ${spirent_running_test_id}

hede 
    Start Packet Capture
    Fetch Pcap Files    ${SPIRENT_TEST_ID}
    Log    hede

*** Keywords ***
Prepare Setup
    [Documentation]    Ansible ile test ortamını hazırlayacağız
    Log To Console    \n<<<-------------- Prepare Setup ---------------->>>


Before Test
    [Documentation]    Start TCP Dump
    # ${result}=    Run Process    ansible-playbook    playbooks/KT_CN_001.yml
    Copy Ssh Id To Servers
    Get Installed Packages And Versions
    Start Packet Capture
    Log    hede
After Test 
    Fetch Pcap Files    ${SPIRENT_TEST_ID}
    Log    hede