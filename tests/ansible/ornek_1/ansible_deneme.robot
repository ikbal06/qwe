*** Settings ***
Library    Process
Library    Collections
Library    OperatingSystem


*** Test Cases ***
Run External Process
    [Documentation]    Run an external process using Run Process keyword. output'un değeri > '"Hello, Robot Framework" '
    [Tags]    external-process
    # Run And Return Rc ile veya
    ${result} =    Run And Return Rc    echo "Hello, Robot Framework"
    Should Be Equal As Integers    ${result}    0
    # OperatingSystem.Run ile
    ${pwd} =    OperatingSystem.Run    pwd
    Log    ${pwd}
    Should Be Equal As Strings    ${pwd.strip()}    /workspace

Run Ansible Playbook with process
    [Documentation]    Run the Ansible playbook to print "Hello World".
    [Tags]    ansible
    ${result} =    Run Process    cat    tests/ansible/ornek_1/ansible_deneme.yaml
    Should Be Equal As Strings    ${result.rc}    0

Run Ansible Playbook with ansible-runner
    [Documentation]    Run an Ansible playbook using ansible-playbook.
    [Tags]    ansible
    ${result} =    Run Ansible Playbook    tests/ansible/ornek_1/ansible_deneme.yaml
    Log    ${result.stdout}
    Log    ${result.stderr}
    #Should Be Equal As Integers    ${result.rc}    0

ansible-playbook yüklü ve çalışıyor
    [Documentation]    Run the Ansible playbook to print "Hello World" in the console.
    [Tags]    ansible
    ${result} =    Run Process    ansible-playbook    --version
    Log    ${result.stdout}
    Log    ${result.stderr}
    ${expected_status_code} =    Convert To Integer    0
    ${actual_status_code} =    Convert To Integer    ${result.rc}
    Should Be Equal    ${actual_status_code}    ${expected_status_code}

ansible-playbook ile task koş
    [Documentation]    Run the Ansible playbook to print "Hello World" in the console.
    [Tags]    ansible
    ${result} =    Run Process    ansible-playbook    tests/ansible/ornek_1/ansible_deneme.yaml
    Log    Çıktı: ${result.stdout}

ansible-runner Playbook
    [Documentation]    Run an Ansible playbook using ansible-runner.
    [Tags]    ansible

    # Ansible-runner ile playbook'ı çağır
    ${command} =    Set Variable    ansible-runner    run    tests/ansible/ornek_1    -p    ansible_deneme.yaml

    # Komutu çalıştır
    ${output} =    Run Process    ${command}
    Log    ${output.stdout}

    # Çıkış kodunu kontrol et
    Should Be Equal As Integers    ${output.rc}    0


*** Keywords ***
Run Ansible Playbook
    [Arguments]    ${playbook_name}
    ${ansible_runner_cmd} =    Set Variable    ansible-runner run ${playbook_name}
    ${result} =    Run Process    ${ansible_runner_cmd}    shell=True    stdout=PIPE    stderr=PIPE
    ${output} =    Convert To String    ${result.stdout}
    Log    Ansible Runner Output: ${output}
    RETURN    ${result}
