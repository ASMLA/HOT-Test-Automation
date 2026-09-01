*** Settings ***
Library    Collections
Library    String

*** Keywords ***
Validate Required Test Data Fields
    [Documentation]    Verifies that all required keys exist and have non-empty values.
    [Arguments]    ${record}    @{required_fields}
    FOR    ${field}    IN    @{required_fields}
        Dictionary Should Contain Key    ${record}    ${field}
        ${value}=    Get From Dictionary    ${record}    ${field}
        Should Not Be Empty    ${value}    msg=Required test-data field '${field}' must not be empty.
    END

Validate Automation Test Identifier
    [Documentation]    Ensures generated records are traceable as automation-created data.
    [Arguments]    ${identifier}
    Should Start With    ${identifier}    AUTO_

Validate Non Production Email
    [Documentation]    Prevents the generic test-data generator from producing a real email domain by default.
    [Arguments]    ${email}
    Should End With    ${email}    @example.test
