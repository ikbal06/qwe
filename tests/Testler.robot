# *** Test Cases ***

# Test Run
#    ${file_list}    Create List    KT_CN_001.robot   
#    FOR    ${file}    IN    @{file_list}
#    Run Keyword And Continue On Failure    Run Test1    ${file}
#    END

# *** Keywords ***
# Run Test1 
#    [Arguments]    ${file_name}
#    Log To Console    Running test filse: ${file_name}
#    Run Keyword If    'KT_CN_001.robot'==${file_name}    File1 Keyword
#    Run Keyword If    'KT_CN_002.robot'==${file_name}    File2 Keyword

# File1 Keyword
#    Set Global Variable    ${TEST_ID}

# File2 Keyword
#    Set Global Variable    ${TEST_ID}


# *** Settings ***
# Test Template    Run Test With Data

# *** Test Cases ***
# Test Case 1
#    ${data}    Set Test Variable    TEST_ID
#    Log    Test Data: ${data}

# Test Case 2
#    ${data}    Set Test Variable    TEST_ID
#    Log    Test Data: ${data}

# *** Keywords ***
# Run Test With Data
#    [Arguments]    ${data}
#    Log    Running Test With Data: ${data}

*** Test Cases ***
Set Robot File Name
    ${file_name}    Set Robot File Name
    Log    Robot File Name: ${file_name}
    Run Keyword And Continue On Failure    Run Robot Test File    ${file_name}

*** Keywords ***
Set Robot File Name
    ${file_name}    Run Keyword    Evaluate    "KT_CN_" + "001" + ".robot"    # Dosya adını dinamik olarak oluşturun (örnekte "test1.robot" olarak varsayıyoruz)
    Set Suite Variable    ${file_name}

*** Keywords ***
Run Robot Test File
    [Arguments]    ${file_name}
    Log    Running test file: ${file_name}
    Run Keyword If    "${file_name}" == "KT_CN_001.robot"    Run Test 1
    Run Keyword If    "${file_name}" == "KT_CN_002.robot"    Run Test 2
    # Diğer test dosyaları için benzer kontrolleri ekleyin

Run Test 1
    # test1.robot dosyası için gerekli işlemleri burada yapın

Run Test 2
    # test2.robot dosyası için gerekli işlemleri burada yapın

*** Keywords ***
Run Robot Test File
    [Arguments]    ${file_name}
    Log    Running test file: ${file_name}
    Run Test    ${file_name}
