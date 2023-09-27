*** Variables ***
${SPIRENT_TEST_ID}    
${SPIRENT_SERVER_NAME}
${RUNNING_TEST_ID}
# ${SPIRENT_RUNNING_TEST_ID}

*** Settings ***
Library    Process
Library    OperatingSystem
Library    common/CommonOperations.py
Library    spirent.SpirentManager    WITH NAME    spirentManager
Library    TestConfigOperations    test_name=${SPIRENT_TEST_ID}    ts_name=${SPIRENT_SERVER_NAME}    WITH NAME    testConfig

*** Keywords ***
Is Spirent Ready
    [Documentation]    Spirent lisanslarından boşta olanı var mı?
    [Arguments]    ${_spirent_server_name}
    ${testServer}=    spirentManager.Get Spirent Test Server By Name    server_name=${_spirent_server_name}
    ${state}=    Set Variable If    '${testServer["state"]}' == 'READY'    True    False
    Log To Console    \nSpirent state is: ${state}\n    console=yes
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
    [Arguments]    ${_test_id}    
    ${lib_id}=    spirentManager.Get Library Id By Spirent User Or Exit
    ${spirent_running_test_id}=    spirentManager.Run Test On Spirent    ${lib_id}    ${_test_id}
    ${log_message}=    Catenate    SEPARATOR=    Koşan Test ID:    ${spirent_running_test_id}
    Log    ${log_message}
    Return From Keyword    ${spirent_running_test_id}

Check Status Until Test Is Completed
    [Documentation]    Spirent üzerinde koşulan testin tamamlanıncaya kadar beklenmesi gerekir. 
    ...    Test tamamlanınca TEST STATUS bilgisi dönülür
    ...    Testin 30 dakika süreceği düşünülerek testin başlangıcından itibaren 20 saniye aralıklarla
    ...    testin durumu kontrol edilir. Eğer test COMPLETE veya COMPLETE_ERROR durumuyla tamamlanmışsa
    ...    testin durumu geri dönülür.
    ...    30 Dakika sonunda hala durumu COMPLETE haricinde bir değerdeyse o değerle dönülür.
    [Arguments]    ${spirent_running_test_id}
    ${test_start_time}=    Evaluate    time.time()
    ${limit_minutes}=    Set Variable    30
    ${current_time}=    Evaluate    time.time()
    ${test_stop_time}=    Evaluate    ${test_start_time} + ${limit_minutes * 60}
    WHILE    ${current_time} < ${test_stop_time}
        ${current_time}=    Evaluate    time.time()
        ${test_status}=    spirentManager.Get Test Status    ${spirent_running_test_id}
        # ${test_statuse}=    Set Variable If    "${test_status['testStateOrStep']}" == "COMPLETE"    True    False
        IF    "${test_status['testStateOrStep']}" == "COMPLETE"    BREAK
        IF    "${test_status['testStateOrStep']}" == "COMPLETE_ERROR"    BREAK
        Log    ${test_status['testStateOrStep']}    # x = 1, x = 3
        Sleep    5s
    END
    Return From Keyword    ${test_status}

Test Result Files Spirent
    [Documentation]    Testin sonucunu spirenttan alacağız
    [Arguments]    ${_spirent_running_test_id}    ${dest_path}=/workspace/output
    ${test_status}=    spirentManager.Get Test Status    ${_spirent_running_test_id}
    Log    ${test_status}
    # ${spirent_report_urls}=    Set Variable    ${test_status['resultFilesList']}
    # ${spirent_report_urls}=    Set Variable    ${test_status['criteriaUrl']}
    # FOR    VERI    IN    @{test_status}
    #    criteriaUrl = veri['criteriaUrl']
    # ${spirent_report_urls}=    Set Variable    criteriaUrl

    #    FOR    ${eachURL}    IN    @{spirent_report_urls}
    #    ${command}=    Catenate    wget    ${eachURL}    -P    ${dest_path} 
    #    EVALUATE    subprocess.call('${command}', shell=True)       
    #    END
        
    # END

Test Results
    [Documentation]    Test durumlarını pass fail alacağız
    [Arguments]    ${_spirent_running_test_id}
    ${test_results}=    spirentManager.Get Test Results Json    test_run_id=${_spirent_running_test_id} 
    ${result_summary}=    Set Variable    ''

    FOR    ${each_step}    IN    @{test_results}
        ${status}    Set Variable If    '${each_step["status"]}'    ==    'PASSED'    True    False
        Log    ${status}
        ${test_desc}=    Extract Text Between Parentheses    ${each_step['description']}
        ${test_status}=    Set Variable    ${each_step['status']}
        ${result_summary}=    Catenate    ${result_summary}    \n    [    ${test_status}    ]    ${test_desc}
    END
    Log    Test Summary: ${result_summary}
    Return From Keyword    ${result_summary}


Extract Text Between Parentheses
    [Documentation]    Step içinden testin adını çeker
    [Arguments]    ${description}
    ${description}=    Set Variable    [ PASS if (Ng Setup Requests 1) ]
    ${start_index}=    Evaluate    "${description}".find("(")
    ${end_index}=    Evaluate    "${description}".find(")")
    ${extracted_text}=    Evaluate    "${description}"[${start_index+1}:${end_index}]
    Log    Extracted Text: ${extracted_text}
    Return From Keyword    ${extracted_text}





    


