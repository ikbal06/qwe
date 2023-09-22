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
Library    TestConfigOperations


*** Variables ***
${MESSAGE}    Hello, Dunya!
${TEST_ID}    KT_CN_010
${ALLINONE_IP}    192.168.13.71
${allinone_ip}    allinone_ip
${MONGODB_DEPLOYMENT_TYPE}    cnf
${K8S_NAMESPACE}    default
${POSTGRE_DEPLOYMENT_TYPE}    cnf
${CN_DEPLOYMENT_TYPE}    vnf
${SPIRENT_SERVER_NAME}    vts-VTO2
${N6_IP}    10.10.22.33
${PUBLIC_IP}    10.10.20.22
${H_MCC}    001
${H_MNC}    001

*** Test Cases ***
Sample Test
    [Documentation]    This is a sample test case
    Log    This is a log message

Run Ansible Playbook
    [Documentation]    Run an Ansible playbook using ansible-runner.
    [Tags]    ansible
    ${command} =    Set Variable    ansible-runner 
    ${command1}=    Set Variable    run 
    ${command2} =    Set Variable    tests/ansible/ornek_1  
    ${command3} =    Set Variable    -p  
    ${command4} =    Set Variable    ansible_deneme.yaml
    ${result} =    Run Process    ${command}    ${command1}    ${command2}    ${command3}    ${command4}
    Should Be Equal As Strings    ${result.rc}    0

KT_CN_001-test
    [Documentation]    Runtes an Ansible playbook using the AnsibleLibrary.
    [Tags]    ansible kt_cn_001
    ${result} =    Run Process    ansible-playbook    playbooks/KT_CN_001.yml
    Log    Çıktı: ${result.stdout}

KT_CN_001
    [Documentation]    KT_CN_001 çalışsın
    [Tags]    ansible kt_cn_001
    # Check Connection
    ${isSpirentReady}=    Is Spirent Ready
    Should Be True    ${isSpirentReady}
    Prepare Spirent
    Sut Manager
    # Ortamı Hazırla
    # UE Ekle
    # Servisleri Başlat
    # Test Koş KT_CN_001
    # Sonuçları Analizciye Gönder
    # Sonuçları Epostala



*** Keywords ***
Sonuçları Analizciye RPC ile Gönder
    [Documentation]    Spirent lisanslarından boşta olanı var mı?
    Run Process    echo "Spirent kontrol edilir"

Sonuçları Analizciye REST ile Gönder
    [Documentation]    Analizciye REST ile gönder
    Run Process    echo "Spirent kontrol edilir"

Check Connection
    [Documentation]    common 
    ${check}=    Check Connection   

Is Spirent Ready
    [Documentation]    Spirent lisanslarından boşta olanı var mı?
    ${isSpirentReady}=    Check Test Server    spirent_ts_name_in=${SPIRENT_SERVER_NAME}
    Return From Keyword    ${isSpirentReady}


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
    ${hede}=    Test Session Update Mngr    test_params_in=${EACH_TEST_PARAM}    spirent_ts_param_in=${EACH_SPIRENT_TS_PARAM}    amf_ip_in=${PUBLIC_IP}    upf_ip_in=${N6_IP}    h_mcc_in=${H_MCC}    h_mnc_in=${H_MNC}    spirent_ts_name_in=${SPIRENT_SERVER_NAME}
    Return From Keyword    ${hede}
    
Sut Manager   
    ${get_suts}    Get Suts 
    Return From Keyword    ${get_suts} 
    # Sut Mngr    sut_name_in=    amf_ip_in=


Ortamı Hazırla
    [Documentation]    Hedef sunucuya ÇŞ kuruldu mu?
    Run Process    echo "Spirent kontrol edilir"
    
Ansible Koş
    [Documentation]    KT_CN_001 çalışsın
    [Tags]    ansible kt_cn_001
    #Log    Integer Variable: ${ALLINONE_IP}
    #Should Be Equal As Integers    ${ALLINONE_IP}    192.168.13.71  
    ${result} =    Run Process    cat    inventory/allinone.yml
    ${result} =    Run Process    whereis    ansible-playbook
    ${result} =    Run Process    ansible-playbook    --version 
    Log    ${result.stdout}
    ${command} =    Set Variable    ansible-playbook    
    ${a} =    Set Variable    inventory/allinone.yml
    ${b} =    Set Variable    -e    "allinone_ip=${ALLINONE_IP} mongodb_deployment_type=${MONGODB_DEPLOYMENT_TYPE} postgre_deployment_type=${POSTGRE_DEPLOYMENT_TYPE} k8s_namespace=${K8S_NAMESPACE} cn_deployment_type=${CN_DEPLOYMENT_TYPE}"
    ${result} =    Run Process    ${command}    ${b}    ${a}
    Log    ${result.stdout}

    # robot
    # -t "KT_CN_001"
    # kayitlanma.robot
    # --variable DEFAULT_TEST_LOGS_PATH:"{{spirent_pcap_files_path}}" 
    # --listener zealand.listener.KiwiTCMS 
    # --outputdir "{{robot_files_path}}" 
    # --report "{{test_id}}".html ../Tests/aaaaa.robot

Debug Ansible
    [Documentation]    Run an Ansible playbook using ansible-runner.
    [Tags]    ansible
    ${example_regex}=    catenate    
 ...    ansible-runner
 ...    run
 ...    tests/ansible/ornek_1
 ...    -p
 ...    ansible_deneme.yaml

    ${example_regex1}=    catenate    ansible-runner    run    tests/ansible/ornek_1    -p    ansible_deneme.yaml

    ${command} =    Set Variable    ansible-runner 
    ${command1}=    Set Variable    run 
    ${command2} =    Set Variable    tests/ansible/ornek_1  
    ${command3} =    Set Variable    -p  
    ${command4} =    Set Variable    ansible_deneme.yaml
    # ${result} =    Run Process    ${command}    ${command1}    ${command2}    ${command3}    ${command4}
    ${result} =    Run Process    ${example_regex1}
    Should Be Equal As Strings    ${result.rc}    0
