*** Settings ***
# C:\Users\ikbal.kirklar\Desktop\cem\roles
Library     OperatingSystem
# Library    DenemeListener
Library     MainListener
# Library    KiwiListener
Library     AnsibleLibrary
Library     Process
Library     Collections
Library     OperatingSystem


*** Variables ***
${MESSAGE}                      Hello, Dunya!
${TEST_IID}                     KT_CN_001
${spirent_pcap_files_path}      a
${robot_files_path}             a
${test_id}                      a


*** Test Cases ***
KT_CN_001
    [Documentation]    Run an Ansible playbook using the AnsibleLibrary.
    [Tags]    ansible kt_cn_001
    Run Ansible    playbook    ./playbooks/ULAK5G_core_run_spirent_test.yml

Run Ansible Playbook
    [Documentation]    Run an Ansible playbook using ansible-runner.
    [Tags]    ansible
    ${ansible_result} =    Run Ansible Playbook    my_playbook.yml
    Should Be Equal    ${ansible_result.rc}    0


*** Keywords ***
Run Ansible Playbook
    [Arguments]    ${playbook_name}
    ${ansible_runner_cmd} =    Set Variable    ansible-runner run ${playbook_name}
    ${result} =    Run Process    ${ansible_runner_cmd}    shell=True    stdout=PIPE    stderr=PIPE
    ${output} =    Convert To String    ${result.stdout}
    Log    Ansible Runner Output: ${output}
    RETURN    ${result}
