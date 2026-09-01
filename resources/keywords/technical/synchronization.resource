*** Settings ***
Library     Browser
Resource    ../../variables/resilience.resource

*** Keywords ***
Wait Until Page Is Ready
    [Documentation]    Uses browser-native load-state synchronization instead of fixed sleeps.
    Wait For Load State    ${PAGE_READY_STATE}    timeout=${DEFAULT_UI_TIMEOUT}

Wait Until Element Is Visible
    [Documentation]    Waits for a locator using the central timeout policy.
    [Arguments]    ${locator}    ${timeout}=${DEFAULT_UI_TIMEOUT}
    Wait For Elements State    ${locator}    visible    timeout=${timeout}

Wait Until Element Is Hidden
    [Documentation]    Waits until a transient element is hidden using the central timeout policy.
    [Arguments]    ${locator}    ${timeout}=${DEFAULT_UI_TIMEOUT}
    Wait For Elements State    ${locator}    hidden    timeout=${timeout}

Retry Read Only Check
    [Documentation]    Retries only an idempotent/read-only verification. Never wrap create/update/delete actions with this keyword.
    [Arguments]    ${keyword}    @{args}
    Wait Until Keyword Succeeds    ${READ_RETRY_TIMEOUT}    ${READ_RETRY_INTERVAL}    ${keyword}    @{args}
