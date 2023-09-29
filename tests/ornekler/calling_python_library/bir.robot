*** Settings ***
Library    kutuphane.py

*** Variables ***
${MESSAGE}    Hello, Dunya!

*** Test Cases ***
Testim
    Log    ML: ml
    ${sonuc}=    Beni Cagir    ${MESSAGE}
    Log    Gelen cevap: ${sonuc}