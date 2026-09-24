*** Settings ***
Documentation    Evidências visuais do cenário HOT-INV-DEF-001.
Library          Browser
Library          OperatingSystem
Library          BuiltIn

*** Variables ***
${EVIDENCE_ROOT}       ${EXECDIR}${/}reports${/}evidencias
${EVIDENCE_SCENARIO}   HOT-INV-DEF-001
${EVIDENCE_DIR}        ${EVIDENCE_ROOT}${/}${EVIDENCE_SCENARIO}

*** Keywords ***
Preparar Pasta De Evidencias
    [Documentation]    Limpa somente as evidências da execução anterior deste cenário e recria a pasta.
    Remove Directory    ${EVIDENCE_DIR}    recursive=True
    Create Directory    ${EVIDENCE_DIR}
    Log    Evidências desta execução: ${EVIDENCE_DIR}

Registrar Evidencia
    [Arguments]    ${arquivo}
    [Documentation]    Salva screenshot da página atual dentro da pasta exclusiva do cenário.
    ${destino}=    Set Variable    ${EVIDENCE_DIR}${/}${arquivo}.png
    Take Screenshot    filename=${destino}
    Log    Evidência gravada: ${destino}
    RETURN    ${destino}

Registrar Evidencia Final Do Teste
    [Documentation]    Registra o estado final da página. Se o teste falhar, a imagem preserva a tela do erro.
    ${status}=    Set Variable    ${TEST STATUS}
    IF    '${status}' == 'PASS'
        Registrar Evidencia    99_teste_finalizado_com_sucesso
    ELSE
        Registrar Evidencia    99_erro_estado_final
    END
