*** Settings ***
# C:\Users\ikbal.kirklar\Desktop\cem\roles
Library    OperatingSystem
# Variables  variables.py
Library    resources/kiwi/KiwiListener.py
Library    resources/MainListener.py

*** Variables ***
${MESSAGE}       Hello, world!

*** Test Cases ***
Another Test
    Should Be Equal    ${MESSAGE}    Hello, world!