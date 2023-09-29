*** Settings ***
Test Setup      Before Starting
Test Teardown    After Finished

*** Test Cases ***
Sample Test
    [Documentation]    This is a sample test case
    Log To Console   This is a log message

*** Keywords ***
Before Starting
    Log To Console    >>>> Before Starting

After Finished
    Log To Console    >>>> After Finished