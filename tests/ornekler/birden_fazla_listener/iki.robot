*** Settings ***
Library    Process


*** Variables ***
${MESSAGE}    Hello, Dunya!

*** Test Cases ***
İkinici Test
    [Documentation]    This is a sample test case
    [Tags]    listener    iki 
    Log    This is a log message

*** Keywords ***
Sonuçları Analizciye RPC ile Gönder
    [Documentation]    Spirent lisanslarından boşta olanı var mı?
    Run Process    echo "Spirent kontrol edilir"
