*** Settings ***
Library    Process


*** Variables ***
${MESSAGE}    Hello, Dunya!

*** Test Cases ***
Bir Test
    [Documentation]    This is a sample test case
    Log    This is a log message

*** Keywords ***
Sonuçları Analizciye RPC ile Gönder
    [Documentation]    Spirent lisanslarından boşta olanı var mı?
    Run Process    echo "Spirent kontrol edilir"
