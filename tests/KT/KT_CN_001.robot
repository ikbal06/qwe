# Variables içindeki değişkenler: BÜYÜK HARF
# Keywords metotlarının Arguments: _degisken_adi
# Keywords metotlarının yerel değişkenleri: degisken_adi

*** Settings ***
# Library    listeners/MyListener.py
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

# robot --listener KiwiListener --listener AnalizciListener KTC_CN_001.robot    KTC_CN_002.robot    KTC_CN_007.robot 

*** Test Cases ***
Kayıtlanma Testi [KT_CN_001]
    [Documentation]    Çalıştırılacak testin adı ve ID değeri "KT_CN_001" olacak.
    ...    Çalışacağı Spirent test sunucusu parametre olarak gelebilir 
    ...    Önce Spirent sunucuları arasından arana spirent sunucusu bulunur (yoksa çıkılır -FAIL-)
    ...    Test Oturum Bilgisi Spirent üzerinde güncellenir
    ...    Spirent kullanıcı adı ve koşulacak testin ID bilgisi Spirent üstünde güncellenir
    [Tags]    ansible KT_CN_001
    [Setup]    Prepare Setup
    ${isSpirentReady}=    Is Spirent Ready    ${SPIRENT_SERVER_NAME}
    Should Be True    ${isSpirentReady} 
    ${result}=    Update Test Session    _test_name=${SPIRENT_TEST_ID}    _h_mnc=${H_MNC}    _h_mcc=${H_MCC}    _amf_ip=${AMF_IP}    _upf_ip=${UPF_IP}
    Should Be True    ${result}
    ${SPIRENT_RUNNING_TEST_ID}=    Run Test    ${SPIRENT_TEST_ID}
    ${test_status}=    Check Status Until Test Is Completed    ${SPIRENT_RUNNING_TEST_ID}
    Should Be Equal As Strings    "${test_status['testStateOrStep']}"    "COMPLETE"
    # Copy Test Result Files From Spirent    ${SPIRENT_RUNNING_TEST_ID}



*** Keywords ***
Prepare Setup
    [Documentation]    Ansible ile test ortamını hazırlayacağız
    # Set Environment Variable    RUNNING_TEST_ID    ${RUNNING_TEST_ID}
    # Set Environment Variable    ${SPIRENT_TEST_ID}    PASSED
    Set Global Variable    ${KIWI_PLAN_ID}
    Set Global Variable    ${SPIRENT_TEST_ID}
    Set Global Variable    ${SPIRENT_SERVER_NAME}
    Set Global Variable    ${SPIRENT_RUNNING_TEST_ID}
    ${result}=    Run Process    ansible-playbook    playbooks/KT_CN_001.yml