
*** Settings ***

Library    OperatingSystem
Library    ../resources/MainListener.py

*** Variables ***
${MESSAGE}       Hello, world!

*** Test Cases ***
Another Test
    Should Be Equal    ${MESSAGE}    Hello, world!