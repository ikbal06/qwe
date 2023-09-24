*** Settings ***
Library    Process
Library    OperatingSystem
Library    spirent.SpirentManager    WITH NAME    spirentManager
Library    spirent.SpirentManager
Library    common/CommonOperations.py
Library    TestConfigOperations

*** Keywords ***
Is Spirent Ready
    [Documentation]    Spirent lisanslarından boşta olanı var mı?
    [Arguments]    ${_spirent_server_name}
    ${testServer}=    spirentManager.Get Spirent Test Server By Name    server_name=${_spirent_server_name}
    ${state}=    Set Variable If    '${testServer["state"]}' == 'READY'    True    False
    Return From Keyword    ${state}