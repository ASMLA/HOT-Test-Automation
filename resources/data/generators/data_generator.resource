*** Settings ***
Library    DateTime
Library    String

*** Keywords ***
Generate Unique Token
    [Documentation]    Generates a UUID-based token without adding an external dependency.
    ${token}=    Evaluate    __import__('uuid').uuid4().hex
    RETURN    ${token}

Generate Test Email
    [Documentation]    Generates a unique non-production email address for test-data templates.
    [Arguments]    ${domain}=example.test
    ${token}=    Generate Unique Token
    ${email}=    Set Variable    auto.${token}@${domain}
    RETURN    ${email}

Generate Test Timestamp
    [Documentation]    Generates a compact timestamp suitable for traceable test identifiers.
    ${timestamp}=    Get Current Date    result_format=%Y%m%d%H%M%S%f
    RETURN    ${timestamp}

Generate ISO Timestamp
    [Documentation]    Generates an ISO-like UTC timestamp for metadata stored with generated test data.
    ${timestamp}=    Get Current Date    time_zone=UTC    result_format=%Y-%m-%dT%H:%M:%S.%fZ
    RETURN    ${timestamp}

Generate Test Identifier
    [Documentation]    Generates a traceable AUTO-prefixed identifier for framework-created test records.
    ${timestamp}=    Generate Test Timestamp
    ${token}=    Generate Unique Token
    ${short_token}=    Get Substring    ${token}    0    8
    ${identifier}=    Catenate    SEPARATOR=_    AUTO    ${timestamp}    ${short_token}
    RETURN    ${identifier}
