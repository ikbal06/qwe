*** Variables ***
${SPIRENT_TEST_ID}    KT_CN_008

*** Settings ***
Resource    keywords/spirent.robot  
Library    String 
Test Teardown    After Test    


*** Test Cases ***


UE Tarafından Başlatılan Kayıt Silme [KT_CN_008]
    [Documentation]    Çalıştırılacak testin adı ve ID değeri "KT_CN_008" olacak.
    ...    Çalışacağı Spirent test sunucusu parametre olarak gelebilir 
    ...    Önce Spirent sunucuları arasından arana spirent sunucusu bulunur (yoksa çıkılır -FAIL-)
    ...    Test Oturum Bilgisi Spirent üzerinde güncellenir
    ...    Spirent kullanıcı adı ve koşulacak testin ID bilgisi Spirent üstünde güncellenir
    [Tags]    ansible    BT CN 008
    [Setup]    Prepare Setup
    Log To Console    ****************
    ${result}=    Prepare Spirent    ${SPIRENT_TEST_ID}
    Should Be True    ${result}
    Before Test
    ${spirent_running_test_id}=    Run Spirent Test Server    ${SPIRENT_TEST_ID}
    ${test_status}=    Check Status Until Test Is Completed    ${spirent_running_test_id}
    Set Global Variable    ${test_status}
    Log To Console    ${test_status}
    Should Be Equal As Strings    "${test_status['testStateOrStep']}"    "COMPLETE"
    Copy Test Result Files From Spirent    ${spirent_running_test_id}


*** Keywords ***
Prepare Setup
    [Documentation]    Ansible ile test ortamını hazırlayacağız
    Log To Console    \n<<<-------------- Prepare Setup ---------------->>>



    