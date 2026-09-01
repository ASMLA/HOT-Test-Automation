*** Settings ***
Library     Browser
Resource    ../../keywords/technical/browser_keywords.resource
Resource    ../../keywords/technical/synchronization.resource
Resource    ../../variables/resilience.resource

*** Keywords ***
Open Application Page And Validate Health
    [Documentation]    Page-layer operation that opens an application, validates its URL, and checks known technical failures.
    [Arguments]    ${url}    ${expected_url_fragment}
    New Page    ${url}
    Wait Until Page Is Ready
    Get Url    contains    ${expected_url_fragment}
    Validate Page Has No Known Technical Errors

Validate Application Root Is Visible
    [Documentation]    Page-layer assertion that a stable application root is visible.
    [Arguments]    ${page_locator}
    Wait Until Element Is Visible    ${page_locator}

Get First Visible Page Locator
    [Documentation]    Returns the first visible locator from an ordered primary-to-fallback list.
    [Arguments]    @{locators}
    FOR    ${locator}    IN    @{locators}
        ${is_visible}=    Run Keyword And Return Status
        ...    Wait Until Element Is Visible    ${locator}    ${SHORT_UI_TIMEOUT}
        IF    ${is_visible}
            RETURN    ${locator}
        END
    END
    Fail    None of the candidate locators became visible: ${locators}
