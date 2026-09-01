*** Settings ***
Documentation    Shared reporting, evidence, and execution-observability helpers.
Library          OperatingSystem
Library          Collections
Library          String
Resource         ../../variables/observability.resource
Resource         configuration.resource
Resource         logging.resource

*** Keywords ***
Resolve Evidence Root
    ${root}=    Get Configuration Value    EVIDENCE_ROOT    ${DEFAULT_EVIDENCE_ROOT}
    RETURN    ${root}

Resolve Report Root
    ${root}=    Get Configuration Value    REPORT_ROOT    ${DEFAULT_REPORT_ROOT}
    RETURN    ${root}

Create Execution Evidence Directory
    [Arguments]    ${execution_id}
    ${root}=    Resolve Evidence Root
    ${path}=    Join Path    ${root}    ${execution_id}
    Create Directory    ${path}
    RETURN    ${path}

Build Evidence File Name
    [Arguments]    ${execution_id}    ${artifact_type}    ${extension}
    ${safe_type}=    Replace String Using Regexp    ${artifact_type}    [^A-Za-z0-9_-]    _
    ${file_name}=    Set Variable    ${execution_id}_${safe_type}.${extension}
    RETURN    ${file_name}

Create Execution Metadata
    [Arguments]    ${execution_id}    ${scope}    ${status}=UNKNOWN
    ${metadata}=    Create Dictionary
    ...    schema_version=${OBSERVABILITY_SCHEMA_VERSION}
    ...    execution_id=${execution_id}
    ...    scope=${scope}
    ...    status=${status}
    RETURN    ${metadata}

Log Execution Metadata
    [Arguments]    ${metadata}
    ${execution_id}=    Get From Dictionary    ${metadata}    execution_id
    ${scope}=    Get From Dictionary    ${metadata}    scope
    ${status}=    Get From Dictionary    ${metadata}    status
    Log Framework Info    execution_id=${execution_id}; scope=${scope}; status=${status}    observability
