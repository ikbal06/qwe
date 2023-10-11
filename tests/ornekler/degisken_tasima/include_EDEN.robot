*** Variables ***
${MESSAGE}    Hello, Venus!


*** Settings ***
Resource    tests/ornekler/degisken_tasima/include_edilen.robot

*** Test Cases ***
Sample Test
    [Documentation]    This is a sample test case
    Log    This is a log message ${MESSAGE}
