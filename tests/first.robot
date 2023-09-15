*** Settings ***
# C:\Users\ikbal.kirklar\Desktop\cem\roles
Library     OperatingSystem
# Library    DenemeListener
Library     MainListener
# Library    KiwiListener


*** Variables ***
${MESSAGE}      Hello, Dunya!
${TEST_IID}     KT_CN_010


*** Test Cases ***
Sample Test
    [Documentation]    This is a sample test case

    Log    This is a log message
