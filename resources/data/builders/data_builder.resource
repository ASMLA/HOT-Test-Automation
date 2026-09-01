*** Settings ***
Library     Collections
Resource    ../generators/data_generator.resource

*** Keywords ***
Build Generic Test Record
    [Documentation]    Builds application-agnostic test data with traceability metadata and optional overrides.
    [Arguments]    &{overrides}
    ${identifier}=    Generate Test Identifier
    ${email}=    Generate Test Email
    ${created_at}=    Generate ISO Timestamp
    ${record}=    Create Dictionary
    ...    id=${identifier}
    ...    email=${email}
    ...    status=READY
    ...    source=AUTOMATION
    ...    created_at=${created_at}
    Set To Dictionary    ${record}    &{overrides}
    RETURN    ${record}

Build Record Missing Required Field
    [Documentation]    Creates a negative-test data record by removing one required field from a valid generic record.
    [Arguments]    ${field_name}
    ${record}=    Build Generic Test Record
    Remove From Dictionary    ${record}    ${field_name}
    RETURN    ${record}
