*** Settings ***
# C:\Users\ikbal.kirklar\Desktop\cem\roles
Library    OperatingSystem
# Library    DenemeListener
Library    MainListener
# Library    KiwiListener
Library    AnsibleLibrary


*** Variables ***
${MESSAGE}    Hello, Dunya!
${TEST_IID}    KT_CN_010


*** Test Cases ***
Sample Test
    [Documentation]    This is a sample test case
    Log    This is a log message

Run Ansible Playbook
    [Documentation]    Run an Ansible playbook using ansible-runner.
    [Tags]    ansible
    ${command} =    Set Variable    ansible-runner    run    tests/ansible/ornek_1    -p    ansible_deneme.yaml
    Should Be Equal As Strings    ${command.rc}    0

KT_CN_001
    [Documentation]    Run an Ansible playbook using the AnsibleLibrary.
    [Tags]    ansible kt_cn_001
    Run Ansible    playbook    my_playbook.yml
