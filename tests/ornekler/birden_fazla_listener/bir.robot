*** Settings ***
Library    Process
Library    resources/kiwi/KiwiListener.py

*** Variables ***
${MESSAGE}    Hello, Dunya!
# KIWI 
${KIWI_TEST_ID}    168
${KIWI_PLAN_ID}    7
# SPIRENT
${SPIRENT_TEST_ID}    KT_CN_001
${SPIRENT_RUNNING_TEST_ID}    
${SPIRENT_SERVER_NAME}    vts-VTO2
${ALLINONE_IP}    192.168.13.71
${MONGODB_DEPLOYMENT_TYPE}    cnf
${K8S_NAMESPACE}    default
${POSTGRE_DEPLOYMENT_TYPE}    cnf
${CN_DEPLOYMENT_TYPE}    vnf
${N6_IP}    10.10.22.33
${UPF_IP}    ${N6_IP}
${PUBLIC_IP}    10.10.20.22
${AMF_IP}    ${PUBLIC_IP}
${H_MCC}    001
${H_MNC}    001

*** Test Cases ***
Testim
    [Documentation]    This is a sample test case
    [Tags]    listener    bir 
    [Setup]    Prepare Setup
    Log    This is a log message


*** Keywords ***
Prepare Setup
    [Documentation]    Ansible ile test ortamını hazırlayacağız
    # Set Environment Variable    RUNNING_TEST_ID    ${RUNNING_TEST_ID}
    # Set Environment Variable    ${SPIRENT_TEST_ID}    PASSED
    Set Global Variable    ${KIWI_PLAN_ID}    7 
    Set Global Variable    ${SPIRENT_TEST_ID}
    Set Global Variable    ${SPIRENT_SERVER_NAME}
    Set Global Variable    ${SPIRENT_RUNNING_TEST_ID}
    ${result}=    Run Process    ansible-playbook    playbooks/KT_CN_001.yml