*** Settings ***
Library          Browser
Documentation    Compatibility resource for versions prior to v0.9.0. New code should import resources/keywords/technical/browser_keywords.resource.
Resource         ../technical/browser_keywords.resource
Resource         ../../pages/common/base_page.resource

*** Keywords ***
Open Application
    [Documentation]    Compatibility alias. New Page Objects should use Open Application Page And Validate Health.
    [Arguments]    ${url}
    New Page    ${url}
    Wait For Load State    domcontentloaded

Validate Current URL
    [Arguments]    ${expected_url_fragment}
    Get Url    contains    ${expected_url_fragment}

Access Application And Validate Health
    [Arguments]    ${url}    ${expected_url_fragment}
    Open Application Page And Validate Health    ${url}    ${expected_url_fragment}

Validate Application Initial Page
    [Arguments]    ${page_locator}
    Validate Application Root Is Visible    ${page_locator}

Get First Visible Locator
    [Arguments]    @{locators}
    ${locator}=    Get First Visible Page Locator    @{locators}
    RETURN    ${locator}
