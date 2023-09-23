*** Settings ***
Library    Process
# C:\Users\ikbal.kirklar\Desktop\cem\roles
Library    OperatingSystem
# Library    DenemeListener
# Library    resources.MainListener
# Library    kiwi.KiwiListener
# Library    AnsibleLibrary
# Library    spirent.SpirentOperations
Library    spirent.SpirentManager
Library    common/CommonOperations.py
Library    TestConfigOperations    test_name=${TEST_ID}    ts_name=${SPIRENT_SERVER_NAME} 
Resource    keywords/spirent.robot


*** Variables ***
${TEST_ID}    KT_CN_001
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
    Update Test Session    _test_name=${TEST_ID}    _h_mnc=${H_MNC}    _h_mcc=${H_MCC}    _amf_ip=${AMF_IP}    _upf_ip=${UPF_IP}
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
    [Documentation]    Spirent üzerinde Test Oturum bilgilerini güncelleyeceğiz.
    [Arguments]    ${_test_name}    ${_h_mnc}    ${_h_mcc}    ${_amf_ip}    ${_upf_ip}    # ${_test_params}    ${_spirent_ts_param}    ${_PUBLIC_IP}    ${_data_network_ip}    ${_h_mcc}    ${_h_mnn}    ${_spirent_ts_name} 
    # Test Parametrelerinden
    ${test_params}    Get Test Params
    ${test_id}=    Set Variable    ${test_params['test_id']}
    ${test_duration}=    Set Variable    ${test_params['test_duration']}
    ${perm_key}=    Set Variable    ${test_params['perm_key']}
    ${op_key}=    Set Variable    ${test_params['op_key']}
    ${msin}=    Set Variable    ${test_params['msin']}
    # Spirent özelliklerinden
    ${spirent_ts_params}    Get Spirent Ts Params
    ${spirent_ts_name}=    Set Variable    ${spirent_ts_params['ts_name']}
    ${spirent_gnb_ip}=    Set Variable    ${spirent_ts_params['spirent_gnb_ip']}
    ${spirent_dn_ip}=    Set Variable    ${spirent_ts_params['spirent_dn_ip']}
    ${spirent_dn_interface}=    Set Variable    ${spirent_ts_params['spirent_dn_interface']}
    ${spirent_gnb_interface}=    Set Variable    ${spirent_ts_params['spirent_gnb_interface']}
    # Spirent üstünden ts_name ile Test Sunucunun ID değerini çekiyoruz
    ${spirentTestServer}=    spirent.SpirentManager.Get Spirent Test Server By Name    server_name=${spirent_ts_name}
    ${spirent_ts_id}=    Set Variable    ${spirentTestServer['id']}
    # 
    ${spirent_library_id}=    spirent.SpirentManager.Get Library Id By Spirent User Or Exit
    ${lib_id}=    Set Variable    ${spirent_library_id}
    ${_amf_ip}=    Set Variable    amf_ip
    ${_h_mnc}=    Set Variable    h_mnc
    ${_h_mcc}=    Set Variable    h_mcc
    ${_upf_ip}=    Set Variable    upf_ip
    # 
    ${ue_id}    Catenate    ${_h_mnc}    ${_h_mcc}    ${msin}
    # amf_ip, spirent_ts_name, test_id, lib_id, h_mnc, h_mcc, test_duration, spirent_ts_id, spirent_gnb_ip, perm_key, op_key, spirent_dn_ip, upf_ip, msin, spirent_dn_interface, spirent_gnb_interface
    # ${data} =    spirent.SpirentManager.Update Test Server Session Or Exit    test_params=${test_params}    spirent_ts_param=${spirent_ts_param}    amf_ip=${PUBLIC_IP}    dn_ip=${N6_IP}    h_mcc=${H_MCC}    h_mnc=${H_MNC}    spirent_ts_name=${SPIRENT_SERVER_NAME} 
    # ${lib_id}=    spirent.SpirentManager.Get Library Id Or Exit
    # spirent.SpirentManager.Run Test Or Exit    spirent_lib_id=${lib_id}    test_name=${_test_name} 

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
