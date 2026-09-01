*** Settings ***
Documentation    Centralized secure runtime configuration helpers.
Library          OperatingSystem
Library          String
Resource         ../../variables/secrets.resource
Resource         logging.resource

*** Keywords ***
Get Optional Secret
    [Arguments]    ${name}    ${default}=${SECRET_NOT_CONFIGURED}
    Validate Secret Name    ${name}
    ${value}=    Get Environment Variable    ${name}    ${default}
    RETURN    ${value}

Get Required Secret
    [Arguments]    ${name}
    Validate Secret Name    ${name}
    ${value}=    Get Environment Variable    ${name}    ${SECRET_NOT_CONFIGURED}
    IF    '${value}' == '${SECRET_NOT_CONFIGURED}' or '${value}' == ''
        Fail    Required secret '${name}' is not configured in the runtime environment.
    END
    RETURN    ${value}

Validate Secret Name
    [Arguments]    ${name}
    ${matches}=    Get Regexp Matches    ${name}    ${SECRET_NAME_PATTERN}
    IF    not ${matches}
        Fail    Invalid secret name '${name}'. Use uppercase environment-style names such as APP_PASSWORD.
    END

Mask Secret
    [Arguments]    ${value}
    IF    '${value}' == ''
        RETURN    ${EMPTY}
    END
    RETURN    ${SECRET_MASK}

Log Secret Availability
    [Arguments]    ${name}
    ${value}=    Get Optional Secret    ${name}
    ${configured}=    Evaluate    $value != $SECRET_NOT_CONFIGURED and $value != ''
    Log Framework Debug    secret=${name}; configured=${configured}    security
    RETURN    ${configured}
