# Variables içindeki değişkenler: BÜYÜK HARF
# Keywords metotlarının Arguments: _degisken_adi
# Keywords metotlarının yerel değişkenleri: degisken_adi

*** Variables ***
# KIWI 
# Bu testin KIWI üstünde karşılığı olan Test Case ID bilgisi

*** Settings ***
# Library    listeners/MyListener.py
Resource    keywords/spirent.robot  
# Library    capturer/pcapCapturer.py
Library    String 
Test Setup    Before Test    #testş hazırlama
Test Teardown    After Test    #testi sonlandırma


*** Test Cases ***

# BOŞ Kayıtlanma Testi [KT_CN_001]
#    Log    Boş boş koş

Kayıtlanma Testi [KT_CN_001]
    [Documentation]    Çalıştırılacak testin adı ve ID değeri "KT_CN_001" olacak.
    ...    Çalışacağı Spirent test sunucusu parametre olarak gelebilir 
    ...    Önce Spirent sunucuları arasından arana spirent sunucusu bulunur (yoksa çıkılır -FAIL-)
    ...    Test Oturum Bilgisi Spirent üzerinde güncellenir
    ...    Spirent kullanıcı adı ve koşulacak testin ID bilgisi Spirent üstünde güncellenir
    [Tags]    ansible    BT CN 001
    [Setup]    Prepare Setup
    ${result}=    Prepare Spirent    ${SPIRENT_TEST_ID}
    Should Be True    ${result}
    ${spirent_running_test_id}=    Run Test    ${SPIRENT_TEST_ID}
    ${test_status}=    Check Status Until Test Is Completed    ${spirent_running_test_id}
    Log To Console    ${test_status}
    Should Be Equal As Strings    "${test_status['testStateOrStep']}"    "COMPLETE"
    Copy Test Result Files From Spirent    ${spirent_running_test_id}

# hede 
#    Start Packet Capture
#    Fetch Pcap Files    ${SPIRENT_TEST_ID}
#    Log    hede

*** Keywords ***
Prepare Setup
    [Documentation]    Ansible ile test ortamını hazırlayacağız
    Log To Console    \n<<<-------------- Prepare Setup ---------------->>>

Before Test
    [Documentation]    Start TCP Dump
    ${result}=    Run Process    ansible-playbook    playbooks/KT_CN_001.yml
    ansibleManager.Copy Ssh Id To Servers
    ansibleManager.Get Installed Packages And Versions
    ansibleManager.Run Test Playbook    ${SPIRENT_TEST_ID}
    ansibleManager.Start Packet Capture
    Log    hede
After Test 
    ansibleManager.Fetch Pcap Files    ${SPIRENT_TEST_ID}
    Log    hede fin
    