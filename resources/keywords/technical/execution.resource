*** Settings ***
Documentation    Shared execution-strategy helpers for local and CI orchestration.
Library          OperatingSystem
Resource         ../../variables/execution.resource
Resource         configuration.resource
Resource         logging.resource

*** Keywords ***
Resolve Parallel Process Count
    ${value}=    Get Configuration Value    PARALLEL_PROCESSES    ${DEFAULT_PARALLEL_PROCESSES}
    ${processes}=    Convert To Integer    ${value}
    IF    ${processes} < 1
        Fail    PARALLEL_PROCESSES must be greater than zero.
    END
    RETURN    ${processes}

Resolve Execution Scope
    ${scope}=    Get Configuration Value    EXECUTION_SCOPE    ${DEFAULT_EXECUTION_SCOPE}
    RETURN    ${scope}

Resolve Parallel Output Directory
    ${output}=    Get Configuration Value    PARALLEL_OUTPUT_DIR    ${DEFAULT_OUTPUT_DIRECTORY}/parallel
    RETURN    ${output}

Log Execution Strategy
    ${processes}=    Resolve Parallel Process Count
    ${scope}=    Resolve Execution Scope
    ${output}=    Resolve Parallel Output Directory
    Log Framework Info    scope=${scope}; processes=${processes}; output=${output}    execution
