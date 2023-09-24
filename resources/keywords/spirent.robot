*** Variables ***
${TEST_ID}    
${SPIRENT_SERVER_NAME}    

*** Settings ***
Library    Process
Library    OperatingSystem
Library    common/CommonOperations.py
Library    spirent.SpirentManager    WITH NAME    spirentManager
Library    TestConfigOperations    test_name=${TEST_ID}    ts_name=${SPIRENT_SERVER_NAME}    WITH NAME    testConfig

*** Keywords ***
Is Spirent Ready
    [Documentation]    Spirent lisanslarından boşta olanı var mı?
    [Arguments]    ${_spirent_server_name}
    ${testServer}=    spirentManager.Get Spirent Test Server By Name    server_name=${_spirent_server_name}
    ${state}=    Set Variable If    '${testServer["state"]}' == 'READY'    True    False
    Return From Keyword    ${state}

Update Test Session    
    [Documentation]    Spirent üzerinde Test Oturum bilgilerini güncelleyeceğiz.
    [Arguments]    ${_test_name}    ${_h_mnc}    ${_h_mcc}    ${_amf_ip}    ${_upf_ip}
    # Test Parametrelerinden    
    ${test_params}    testConfig.Get Test Params By Test Name    ${_test_name}
    ${test_id}=    Set Variable    ${test_params['test_id']}
    ${test_duration}=    Set Variable    ${test_params['test_duration']}
    ${perm_key}=    Set Variable    ${test_params['perm_key']}
    ${op_key}=    Set Variable    ${test_params['op_key']}
    ${msin}=    Set Variable    ${test_params['msin']}
    # Spirent özelliklerinden
    ${spirent_ts_params}    testConfig.Get Spirent Ts Params
    ${spirent_ts_name}=    Set Variable    ${spirent_ts_params['ts_name']}
    ${spirent_gnb_ip}=    Set Variable    ${spirent_ts_params['spirent_gnb_ip']}
    ${spirent_dn_ip}=    Set Variable    ${spirent_ts_params['spirent_dn_ip']}
    ${spirent_dn_interface}=    Set Variable    ${spirent_ts_params['spirent_dn_interface']}
    ${spirent_gnb_interface}=    Set Variable    ${spirent_ts_params['spirent_gnb_interface']}
    # Spirent üstünden ts_name ile Test Sunucunun ID değerini çekiyoruz
    ${spirentTestServer}=    spirentManager.Get Spirent Test Server By Name    server_name=${spirent_ts_name}
    ${spirent_ts_id}=    Set Variable    ${spirentTestServer['id']}
    # 
    ${spirent_library_id}=    spirentManager.Get Library Id By Spirent User Or Exit
    ${lib_id}=    Set Variable    ${spirent_library_id}
    # 
    ${ue_id}    Catenate    ${_h_mnc}    ${_h_mcc}    ${msin}
    # amf_ip, spirent_ts_name, test_id, lib_id, h_mnc, h_mcc, test_duration, spirent_ts_id, spirent_gnb_ip, perm_key, op_key, spirent_dn_ip, upf_ip, msin, spirent_dn_interface, spirent_gnb_interface
    ${data} =    spirentManager.Update Test Server Session Or Exit    ${test_id}    ${_amf_ip}    ${_upf_ip}  
    ...    ${test_duration}    ${spirent_ts_name}    ${spirent_ts_id}    ${spirent_gnb_ip}    ${spirent_dn_ip}    ${spirent_dn_interface}    ${spirent_gnb_interface}  
    ...    ${h_mnc}    ${h_mcc}    ${perm_key}    ${op_key}    ${msin}
    ${result} =    Run Keyword And Return Status    Should Be Equal As Strings    "${data['result']}"    "Test Modified"
    # [Return]    ${result}
    Return From Keyword    ${result}
    # Should Be Equal As Strings    "${data['result']}"    == "Test Modified"
    # spirent.SpirentManager.Run Test Or Exit    spirent_lib_id=${lib_id}    test_name=${_test_name} 

Run Test
    [Documentation]    Spirent üzerinde testin koşulmasını başlat
    ${lib_id}=    spirentManager.Get Library Id By Spirent User Or Exit
    ${running_test_id} =    spirentManager.Run Test On Spirent    ${lib_id}    ${test_id}
    ${log_message}=    Catenate    SEPARATOR=    Koşan Test ID:    ${running_test_id}
    Log    ${log_message}
    Return From Keyword    ${running_test_id}    

Check Status Until Test Is Completed
    [Arguments]    ${running_test_id}
    ${test_start_time}=    Evaluate    time.time()
    ${limit_minutes}=    Set Variable    30
    ${current_time}=    Evaluate    time.time()
    ${test_stop_time}=    Evaluate    ${test_start_time} + ${limit_minutes * 60}
    WHILE    ${current_time} < ${test_stop_time}
        ${current_time}=    Evaluate    time.time()
        ${test_status}=    spirentManager.Get Test Status    ${running_test_id}
        IF    "${test_status['testStateOrStep']}" == "COMPLETE"    BREAK
        IF    "${test_status['testStateOrStep']}" == "COMPLETE_ERROR"    BREAK
        Log    ${test_status['testStateOrStep']}    # x = 1, x = 3
        Sleep    10s
    END
    Return From Keyword    ${test_status}

