*** Settings ***
Documentation    Generic API client contract for future application adapters.
Library          RequestsLibrary
Resource         ../../variables/api.resource
Resource         ../../keywords/technical/logging.resource

*** Keywords ***
Create Generic API Session
    [Arguments]    ${alias}    ${base_url}    ${verify_tls}=${API_VERIFY_TLS}
    Log Framework Debug    Creating API session    alias=${alias}
    Create Session    ${alias}    ${base_url}    verify=${verify_tls}

GET Resource
    [Arguments]    ${alias}    ${uri}    ${expected_status}=200
    Log Framework Debug    GET ${uri}    api=${alias}
    ${response}=    GET On Session    ${alias}    ${uri}    expected_status=${expected_status}
    RETURN    ${response}

POST Resource
    [Arguments]    ${alias}    ${uri}    ${payload}    ${expected_status}=201
    Log Framework Debug    POST ${uri}    api=${alias}
    ${response}=    POST On Session    ${alias}    ${uri}    json=${payload}    expected_status=${expected_status}
    RETURN    ${response}

DELETE Resource
    [Arguments]    ${alias}    ${uri}    ${expected_status}=204
    Log Framework Debug    DELETE ${uri}    api=${alias}
    ${response}=    DELETE On Session    ${alias}    ${uri}    expected_status=${expected_status}
    RETURN    ${response}
