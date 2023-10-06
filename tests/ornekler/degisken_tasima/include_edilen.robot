*** Variables ***
${MESSAGE}
# ${MESSAGE}    Hello, Dunya!

*** Settings ***
Library    ./NesneUretenLib.py    ${MESSAGE}



*** Keywords ***
Nesneyi Yazdır
    [Documentation]    This is a sample test case
    Yazdir
    Log    Nesnenin mesajı yazdırıldı


