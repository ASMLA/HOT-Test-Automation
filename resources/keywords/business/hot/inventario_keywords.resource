*** Settings ***
Documentation    Keywords de negócio do inventário usando apenas ações/locators confirmados no Codegen real.
Library          Collections
Library          String
Library          OperatingSystem
Resource         ../../../pages/hot/inventario_page.resource
Resource         ../../../data/generators/data_generator.resource

*** Keywords ***
Gerar Serial Sequencial Curto
    [Documentation]    Gera serial curto e sequencial no formato AUTO-001, AUTO-002, etc. O contador persiste entre execuções locais.
    ${pasta_contador}=    Set Variable    ${EXECDIR}${/}.test-runtime
    ${arquivo_contador}=    Set Variable    ${pasta_contador}${/}serial_counter.txt
    Create Directory    ${pasta_contador}
    ${existe}=    Run Keyword And Return Status    File Should Exist    ${arquivo_contador}
    IF    ${existe}
        ${atual}=    Get File    ${arquivo_contador}
        ${atual}=    Strip String    ${atual}
        ${proximo}=    Evaluate    int($atual) + 1
    ELSE
        ${proximo}=    Set Variable    1
    END
    Create File    ${arquivo_contador}    ${proximo}
    ${sequencial}=    Evaluate    f"{int($proximo):03d}"
    ${serial}=    Set Variable    AUTO-${sequencial}
    RETURN    ${serial}

Gerar Massa Do Ativo DEF-001
    ${armario}=    Generate Random String    7    [LETTERS][NUMBERS]
    ${ativo}=    Generate Random String    10    [NUMBERS]
    ${chamado}=    Generate Random String    9    [NUMBERS]
    ${chamado_fornecedor}=    Generate Random String    7    [NUMBERS]
    ${serial}=    Gerar Serial Sequencial Curto
    &{massa}=    Create Dictionary
    ...    armario=${armario}
    ...    numero_ativo=${ativo}
    ...    serial=${serial}
    ...    chamado_hitss=${chamado}
    ...    chamado_fornecedor=${chamado_fornecedor}
    RETURN    ${massa}

Acessar Controle De Inventário
    Abrir Home Do HOT
    Abrir Controle De Inventário

Cadastrar Nota Fiscal Do Inventário
    Abrir Novo Inventário Em Popup
    Cadastrar Primeira Nota Fiscal Com Tipo Preenchido

Informar Localização Do Equipamento
    Preencher Localização Confirmada Pelo Codegen    Rio de Janeiro

Configurar Equipamento Com Valores Confirmados
    [Documentation]    Seleciona dinamicamente opções válidas existentes nos combos no momento da execução.
    Preencher Configuração Confirmada Pelo Codegen

Incluir Novo Ativo
    [Arguments]    ${massa}
    Incluir Ativo Confirmado Pelo Codegen
    ...    ${massa}[armario]
    ...    ${massa}[numero_ativo]
    ...    ${massa}[serial]

Localizar E Abrir Ativo Criado
    [Arguments]    ${massa}
    Pesquisar E Abrir Ativo Confirmado Pelo Codegen
    ...    ${massa}[serial]
    ...    ${massa}[numero_ativo]

Gerar Massa Do Ativo DEF-002
    [Documentation]    Reutiliza exatamente a geração de massa já validada no DEF-001.
    ${massa}=    Gerar Massa Do Ativo DEF-001
    RETURN    ${massa}

Gerar Massa Do Ativo DEF-003
    [Documentation]    Reutiliza a massa validada e adiciona Número do Pedido e Remessa do Reparo com 10 caracteres alfanuméricos randômicos.
    ${massa}=    Gerar Massa Do Ativo DEF-001
    ${numero_pedido}=    Generate Random String    10    [LETTERS][NUMBERS]
    ${remessa_reparo}=    Generate Random String    10    [LETTERS][NUMBERS]
    Set To Dictionary    ${massa}    numero_pedido=${numero_pedido}
    Set To Dictionary    ${massa}    remessa_reparo=${remessa_reparo}
    RETURN    ${massa}

Gerar Massa Do Ativo DEF-004
    [Documentation]    Reutiliza exatamente a geração de massa já validada do fluxo base.
    ${massa}=    Gerar Massa Do Ativo DEF-001
    RETURN    ${massa}

Gerar Massa Do Ativo DEF-005
    [Documentation]    Reutiliza exatamente a geração de massa já validada do fluxo base.
    ${massa}=    Gerar Massa Do Ativo DEF-001
    RETURN    ${massa}
