*** Settings ***
Library           OperatingSystem
Library     Browser
Resource    ../../variables/environment.resource
Resource    ../../variables/validation.resource
Resource    ../../variables/resilience.resource

*** Keywords ***
Open Browser Session
    [Documentation]    Opens an isolated browser context using the central execution configuration.
    ${headless}=    Resolve Headless Mode
    New Browser    ${BROWSER}    headless=${headless}
    New Context    viewport={'width': 1440, 'height': 900}
    Set Browser Timeout    ${DEFAULT_UI_TIMEOUT}

Close Browser Session
    [Documentation]    Captures evidence when possible and closes the browser without masking the original test result.
    Run Keyword And Ignore Error    Take Screenshot
    Run Keyword And Ignore Error    Close Browser

Validate Page Has No Known Technical Errors
    [Documentation]    Checks the rendered page against the centrally maintained technical-error catalog.
    ${body_text}=    Get Text    body
    FOR    ${error_message}    IN    @{KNOWN_TECHNICAL_ERRORS}
        Should Not Contain    ${body_text}    ${error_message}
    END

Validate Page Has No Known Technical Error
    [Documentation]    Backward-compatible alias maintained for earlier framework consumers.
    Validate Page Has No Known Technical Errors


Resolve Headless Mode
    [Documentation]    Resolves browser visibility from HEADLESS environment variable. Defaults to false for local execution.
    ${headless_env}=    Get Environment Variable    HEADLESS    false
    ${headless}=    Evaluate    str($headless_env).lower() in ('1','true','yes','on')
    RETURN    ${headless}
