*** Settings ***
Library    listeners.MyListener
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
    Set Global Variable    ${SPIRENT_SERVER_NAME}
    ${isSpirentReady}=    Is Spirent Ready    ${SPIRENT_SERVER_NAME}
    Should Be True    ${isSpirentReady} 
    ${result} =    Update Test Session    _test_name=${TEST_ID}    _h_mnc=${H_MNC}    _h_mcc=${H_MCC}    _amf_ip=${AMF_IP}    _upf_ip=${UPF_IP}
    Should Be True    ${result}
    ${running_test_id} =    Run Test
    ${test_status}=    Check Status Until Test Is Completed    ${running_test_id}
    Should Not Be Empty    ${test_status}
