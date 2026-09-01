*** Settings ***
Library    Collections

*** Variables ***
@{TEST_DATA_CLEANUP_REGISTRY}

*** Keywords ***
Register Test Data For Cleanup
    [Documentation]    Registers a created test-data identifier for later application-specific cleanup.
    [Arguments]    ${identifier}
    Append To List    ${TEST_DATA_CLEANUP_REGISTRY}    ${identifier}

Get Registered Test Data For Cleanup
    [Documentation]    Returns a copy of the identifiers waiting for cleanup.
    ${registered}=    Copy List    ${TEST_DATA_CLEANUP_REGISTRY}
    RETURN    ${registered}

Clear Test Data Cleanup Registry
    [Documentation]    Clears the in-memory registry after cleanup has completed.
    Evaluate    $TEST_DATA_CLEANUP_REGISTRY.clear()
