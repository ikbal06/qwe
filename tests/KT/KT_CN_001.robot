# Variables içindeki değişkenler: BÜYÜK HARF
# Keywords metotlarının Arguments: _degisken_adi
# Keywords metotlarının yerel değişkenleri: degisken_adi

*** Variables ***
# KIWI 
# Bu testin KIWI üstünde karşılığı olan Test Case ID bilgisi
# ${KIWI_TEST_ID}    168
# Bu testin SPIRENT üstünde koşturulacağı Spirent Test ID bilgisi 
${SPIRENT_TEST_ID}    KT_CN_001
${MONGODB_DEPLOYMENT_TYPE}    cnf
${K8S_NAMESPACE}    default
${POSTGRE_DEPLOYMENT_TYPE}    cnf
${CN_DEPLOYMENT_TYPE}    vnf
${H_MCC}    001
${H_MNC}    001

*** Settings ***
# Library    listeners/MyListener.py
Resource    keywords/spirent.robot  
Library    String 



*** Test Cases ***
Kayıtlanma Testi [KT_CN_001]
    [Documentation]    Çalıştırılacak testin adı ve ID değeri "KT_CN_001" olacak.
    ...    Çalışacağı Spirent test sunucusu parametre olarak gelebilir 
    ...    Önce Spirent sunucuları arasından arana spirent sunucusu bulunur (yoksa çıkılır -FAIL-)
    ...    Test Oturum Bilgisi Spirent üzerinde güncellenir
    ...    Spirent kullanıcı adı ve koşulacak testin ID bilgisi Spirent üstünde güncellenir
    [Tags]    ansible    BT CN 001
    [Setup]    Prepare Setup
    ${isSpirentReady}=    Is Spirent Ready    ${SPIRENT_SERVER_NAME}
    Should Be True    ${isSpirentReady} 
    ${result}=    Update Test Session    _spirent_server_name=${SPIRENT_SERVER_NAME}    _test_name=${SPIRENT_TEST_ID}    _h_mnc=${H_MNC}    _h_mcc=${H_MCC}    _amf_ip=${AMF_IP}    _upf_ip=${UPF_IP}
    Should Be True    ${result}
    ${SPIRENT_RUNNING_TEST_ID}=    Run Test    ${SPIRENT_TEST_ID}
    ${test_status}=    Check Status Until Test Is Completed    ${SPIRENT_RUNNING_TEST_ID}
    Should Be Equal As Strings    "${test_status['testStateOrStep']}"    "COMPLETE"
    # Copy Test Result Files From Spirent    ${SPIRENT_RUNNING_TEST_ID}



*** Keywords ***
Prepare Setup
    [Documentation]    Ansible ile test ortamını hazırlayacağız
    Global Setup
    Set Global Variable    ${SPIRENT_TEST_ID}    KT_CN_001
    # ${result}=    Run Process    ansible-playbook    playbooks/KT_CN_001.yml