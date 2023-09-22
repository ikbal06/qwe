*** Settings ***
Library    Process
# C:\Users\ikbal.kirklar\Desktop\cem\roles
Library    OperatingSystem
# Library    DenemeListener
# Library    resources.MainListener
# Library    kiwi.KiwiListener
# Library    AnsibleLibrary
Library    spirent.SpirentOperations
Library    spirent.SpirentManager
Library    common/CommonOperations.py
Library    TestConfigOperations    test_name=${TEST_ID}    ts_name=${SPIRENT_SERVER_NAME} 
Resource    keywords/spirent.robot


*** Variables ***
${TEST_ID}    KT_CN_001
${SPIRENT_SERVER_NAME}    vts-VTO2
${ALLINONE_IP}    192.168.13.71
${allinone_ip}    allinone_ip
${MONGODB_DEPLOYMENT_TYPE}    cnf
${K8S_NAMESPACE}    default
${POSTGRE_DEPLOYMENT_TYPE}    cnf
${CN_DEPLOYMENT_TYPE}    vnf
${N6_IP}    10.10.22.33
${PUBLIC_IP}    10.10.20.22
${H_MCC}    001
${H_MNC}    001

*** Test Cases ***
KT_CN_001
    [Documentation]    '''Çalıştırılacak testin adı ve ID değeri "KT_CN_001" olacak.
    ...    Çalışacağı Spirent test sunucusu parametre olarak gelebilir 
    ...    Önce Spirent sunucuları arasından arana spirent sunucusu bulunur (yoksa çıkılır -FAIL-)
    ...    Test Oturum Bilgisi Spirent üzerinde güncellenir
    ...    Spirent kullanıcı adı ve koşulacak testin ID bilgisi Spirent üstünde güncellenir
    ...    '''
    [Tags]    ansible KT_CN_001
    # Check Connection
    ${isSpirentReady}=    Is Spirent Ready    ${SPIRENT_SERVER_NAME}
    Should Be True    ${isSpirentReady} 
    Update Test Session
    Prepare Spirent
    Sut Manager
    # Ortamı Hazırla
    # UE Ekle
    # Servisleri Başlat
    # Test Koş KT_CN_001
    # Sonuçları Analizciye Gönder
    # Sonuçları Epostala



*** Keywords ***
Update Test Session    
    [Documentation]    Spirent üzerinde Test Oturum bilgilerini güncelleyeceğiz
    ${lib_id}=    spirent.SpirentManager.Get Library Id Or Exit
    ${spirent_ts_param}    Get Spirent Ts Params    
    ${test_params}    Get Test Params
    ${data} =    spirent.SpirentManager.Update Test Server Session    test_params=${test_params}    spirent_ts_param=${spirent_ts_param}    amf_ip=${PUBLIC_IP}    dn_ip=${N6_IP}    h_mcc=${H_MCC}    h_mnc=${H_MNC}    spirent_ts_name=${SPIRENT_SERVER_NAME} 
    spirent.SpirentManager.Render Test Session Template    lib_id=${lib_id}    test_params=${test_params}    spirent_ts_param=${SPIRENT_SERVER_NAME} 

Sonuçları Analizciye RPC ile Gönder
    [Documentation]    Spirent lisanslarından boşta olanı var mı?
    Run Process    echo "Spirent kontrol edilir"

Sonuçları Analizciye REST ile Gönder
    [Documentation]    Analizciye REST ile gönder
    Run Process    echo "Spirent kontrol edilir"

Check Connection
    [Documentation]    common 
    ${check}=    Check Connection   



Prepare Spirent 2
    [Documentation]    Spirent'ı testler için koşuya hazırlar
    spirent.SpirentManager.Update Test Session    ${SPIRENT_SERVER_NAME}    ${TEST_ID}    data=data

Run Tests on Spirent
    [Documentation]    Spirent'ı testler için koşuya hazırlar

Prepare Spirent
    [Documentation]    Spirent test oturumu güncellenir
    ${EACH_SPIRENT_TS_PARAM}    Get Spirent Ts Params    
    ${EACH_TEST_PARAM}    Get Test Params
    Return From Keyword    ${EACH_SPIRENT_TS_PARAM}
    Return From Keyword    ${EACH_TEST_PARAM}
    ${hede}=    Test Session Update Mngr    test_params_in=${EACH_TEST_PARAM}    spirent_ts_param_in=${EACH_SPIRENT_TS_PARAM}    amf_ip_in=${PUBLIC_IP}    dn_ip=${N6_IP}    h_mcc_in=${H_MCC}    h_mnc_in=${H_MNC}    spirent_ts_name_in=${SPIRENT_SERVER_NAME}
    Return From Keyword    ${hede}
    
Sut Manager   
    ${get_suts}    Get Suts 
    Return From Keyword    ${get_suts} 
    # Sut Mngr    sut_name_in=    amf_ip_in=
