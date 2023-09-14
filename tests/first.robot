
*** Settings ***

Library    OperatingSystem
# Variables  variables.py
Library    resources/kiwi/KiwiListener.py

*** Variables ***
${MESSAGE}       Hello, world!

*** Test Cases ***
Another Test
    Should Be Equal    ${MESSAGE}    Hello, world!