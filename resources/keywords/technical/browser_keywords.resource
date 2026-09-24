*** Settings ***
Documentation    Capacidades técnicas compartilhadas de navegador para o HOT.
Library          Browser
Library          OperatingSystem

*** Variables ***
${BROWSER_PROFILE_DIR}    ${EXECDIR}${/}.browser-profile
${BROWSER_TYPE}           chromium
${BROWSER_HEADLESS}       False
${BROWSER_TIMEOUT}        15s

*** Keywords ***
Open Browser Session
    [Documentation]    Abre um contexto persistente do Chromium para reutilizar cookies/local storage entre execuções.
    Create Directory    ${BROWSER_PROFILE_DIR}
    New Persistent Context
    ...    userDataDir=${BROWSER_PROFILE_DIR}
    ...    browser=${BROWSER_TYPE}
    ...    headless=${BROWSER_HEADLESS}
    ...    timeout=${BROWSER_TIMEOUT}
    Set Browser Timeout    ${BROWSER_TIMEOUT}

Close Browser Session
    [Documentation]    Fecha a sessão ao final do teste. O perfil persistente permanece em disco para a próxima execução.
    Close Browser    ALL

Abrir Sessão Persistente Do HOT
    [Documentation]    Alias em português para uso futuro em suites HOT.
    Open Browser Session
