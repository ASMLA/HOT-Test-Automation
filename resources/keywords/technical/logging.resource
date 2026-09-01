*** Settings ***
Documentation    Shared structured logging and diagnostic evidence keywords.
Resource         ../../variables/logging.resource

*** Keywords ***
Log Framework Info
    [Arguments]    ${message}    ${context}=${EMPTY}
    ${formatted}=    Build Structured Log Message    ${message}    ${context}
    Log    ${formatted}    level=${LOG_LEVEL_INFO}

Log Framework Debug
    [Arguments]    ${message}    ${context}=${EMPTY}
    ${formatted}=    Build Structured Log Message    ${message}    ${context}
    Log    ${formatted}    level=${LOG_LEVEL_DEBUG}

Log Framework Warning
    [Arguments]    ${message}    ${context}=${EMPTY}
    ${formatted}=    Build Structured Log Message    ${message}    ${context}
    Log    ${formatted}    level=${LOG_LEVEL_WARN}

Log Framework Error
    [Arguments]    ${message}    ${context}=${EMPTY}
    ${formatted}=    Build Structured Log Message    ${message}    ${context}
    Log    ${formatted}    level=${LOG_LEVEL_ERROR}

Build Structured Log Message
    [Arguments]    ${message}    ${context}=${EMPTY}
    ${has_context}=    Evaluate    bool($context)
    IF    ${has_context}
        RETURN    ${LOG_PREFIX} ${LOG_CONTEXT_SEPARATOR} ${context} ${LOG_CONTEXT_SEPARATOR} ${message}
    END
    RETURN    ${LOG_PREFIX} ${LOG_CONTEXT_SEPARATOR} ${message}

Log Test Start
    [Arguments]    ${test_name}
    Log Framework Info    Test started    test=${test_name}

Log Test End
    [Arguments]    ${test_name}    ${status}
    Log Framework Info    Test finished; status=${status}    test=${test_name}

Log Diagnostic Context
    [Arguments]    ${key}    ${value}
    Log Framework Debug    ${key}=${value}    diagnostic
