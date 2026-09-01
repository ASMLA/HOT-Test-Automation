*** Settings ***
Documentation    Generic environment and configuration resolution helpers.
Library          OperatingSystem
Resource         ../../variables/configuration.resource
Resource         logging.resource

*** Keywords ***
Get Configuration Value
    [Arguments]    ${name}    ${default}=${EMPTY}    ${required}=${FALSE}
    ${value}=    Get Environment Variable    ${name}    ${default}
    IF    ${required} and '${value}' == ''
        Fail    Required configuration '${name}' is missing.
    END
    Log Framework Debug    ${name} resolved    configuration
    RETURN    ${value}

Resolve Environment Name
    ${environment}=    Get Configuration Value    TEST_ENV    ${DEFAULT_ENVIRONMENT}
    RETURN    ${environment}

Resolve Browser Name
    ${browser}=    Get Configuration Value    BROWSER    ${DEFAULT_BROWSER}
    RETURN    ${browser}

Resolve Headless Configuration
    ${headless_env}=    Get Configuration Value    HEADLESS    ${DEFAULT_HEADLESS}
    ${headless}=    Evaluate    str($headless_env).lower() in ('1','true','yes','on')
    RETURN    ${headless}

Resolve API Timeout
    ${value}=    Get Configuration Value    API_TIMEOUT    ${DEFAULT_API_TIMEOUT}
    ${timeout}=    Convert To Number    ${value}
    RETURN    ${timeout}

Validate Required Configuration
    [Arguments]    @{required_names}
    FOR    ${name}    IN    @{required_names}
        Get Configuration Value    ${name}    required=${TRUE}
    END
