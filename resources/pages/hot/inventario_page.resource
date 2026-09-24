*** Settings ***
Documentation    Page Object do Controle de Inventário do HOT reconstruído a partir do Playwright Codegen do fluxo real DEF-001.
Library          Browser
Library          BuiltIn
Resource         ../../keywords/technical/evidence_keywords.resource

*** Variables ***
${HOT_HOME}                         %{HOT_URL_BASE=https://hotcorphml.globalhitss.com.br}/index/

# HOME / NAVEGAÇÃO — confirmados pelo Codegen
${LOC_MODAL_AVISO}                  css=#note_modal
${LOC_AVISO_OK}                     css=#note_modal >> text=OK
${LOC_TOGGLE_NAVIGATION}            role=button[name="Toggle navigation"]
${LOC_MENU_INFRA}                   role=button[name="Infra"]
${LOC_CONTROLE_INVENTARIO}          role=link[name="Controle de Inventário"]
${LOC_NOVO_INVENTARIO}              role=link[name=" NOVO"]

# CADASTRO — confirmados pelo Codegen
${LOC_ACCORDION_NOTA_FISCAL}        role=button[name="Nota Fiscal"]
${LOC_NOTA_FISCAL}                  css=#invoice
${LOC_TIPO_NOTA_FISCAL}    css=#type_invoice
${LOC_SALVAR}                       role=button[name="Salvar"]

${LOC_ACCORDION_LOCALIZACAO}         role=button[name="Localização do Equipamento"]
${LOC_ORIGEM}                       css=#branch
${LOC_LOCALIZACAO_ATIVO}            role=textbox[name="Localização Atual do Ativo"]
${LOC_ESTADO}                       css=#state

${LOC_ACCORDION_CONFIGURACOES}      text="Configurações do Equipamento"
${LOC_TIPO_EQUIPAMENTO}             css=#type_equipment
${LOC_IMAGEM}                       css=#image
${LOC_FABRICANTE}                   css=#maker
${LOC_MODELO}                       css=#model
${LOC_PROCESSADOR}                  css=#processador
${LOC_GERACAO_PROCESSADOR}          css=#processador_generation
${LOC_MEMORIA}                      css=#memory
${LOC_ARMAZENAMENTO}                css=#storage
${LOC_CAPACIDADE_ARMAZENAMENTO}     css=#storage_capacity

${LOC_ACCORDION_DOCUMENTOS}         role=button[name="Documentos"]
${LOC_ACCORDION_INCLUSAO_ATIVOS}    role=button[name="Inclusão dos Ativos"]
${LOC_ARMARIO}                      role=textbox[name="Armário Armário"]
${LOC_NUMERO_ATIVO}                 role=textbox[name="Número do Ativo"]
${LOC_SERIAL}                       role=textbox[name="Serial da Máquina"]
${LOC_ADICIONAR}                    role=button[name="Adicionar"]
${LOC_DETALHES_ATIVOS}              text="Detalhes dos Números de Ativo/Serial"

${LOC_PESQUISA}    css=#search_inventory
# STATUS — confirmados pelo Codegen
${LOC_STATUS_EM_CADASTRO}           text=STATUS: EM CADASTRO
${LOC_STATUS_EM_ESTOQUE}            text=STATUS: EM ESTOQUE
${LOC_EQUIPAMENTO_FUNCIONAL}        text=Equipamento Funcional
${TXT_STATUS_CADASTRO}              STATUS: EM CADASTRO
${TXT_STATUS_ESTOQUE}               STATUS: EM ESTOQUE
${TXT_EQUIPAMENTO_FUNCIONAL}        Equipamento Funcional

*** Keywords ***
Selecionar Primeira Opção Disponível
    [Arguments]    ${locator}
    [Documentation]    Lê as opções atuais do combo e seleciona a primeira opção com value preenchido. Evita dependência de IDs/values fixos do ambiente.
    Wait For Elements State    ${locator}    visible    timeout=30s
    ${opcoes}=    Get Select Options    ${locator}
    ${valor}=    Evaluate    next(op["value"] for op in $opcoes if op["value"])
    Select Options By    ${locator}    value    ${valor}
    RETURN    ${valor}

Selecionar Primeira Opção Disponível Se Estiver Vazio
    [Arguments]    ${locator}
    [Documentation]    Preserva o valor atual. Se estiver vazio, seleciona a primeira opção válida disponível.
    Wait For Elements State    ${locator}    visible    timeout=30s
    ${selecionados}=    Get Selected Options    ${locator}    value
    ${valor_atual}=    Evaluate    $selecionados[0] if $selecionados else ""
    IF    '${valor_atual}' == ''
        ${valor_atual}=    Selecionar Primeira Opção Disponível    ${locator}
    END
    RETURN    ${valor_atual}

Selecionar Opção Disponível Pelo Texto
    [Arguments]    ${locator}    ${texto_esperado}
    [Documentation]    Procura o texto esperado nas opções atuais do combo e seleciona o value encontrado, sem hardcode do value.
    Wait For Elements State    ${locator}    visible    timeout=30s
    ${opcoes}=    Get Select Options    ${locator}
    ${valor_encontrado}=    Set Variable    ${EMPTY}
    FOR    ${opcao}    IN    @{opcoes}
        ${label}=    Set Variable    ${opcao}[label]
        ${value}=    Set Variable    ${opcao}[value]
        ${contem}=    Run Keyword And Return Status    Should Contain    ${label}    ${texto_esperado}    ignore_case=True
        IF    ${contem}
            ${valor_encontrado}=    Set Variable    ${value}
            BREAK
        END
    END
    Should Not Be Empty    ${valor_encontrado}    Nenhuma opção contendo "${texto_esperado}" foi encontrada no combo.
    Select Options By    ${locator}    value    ${valor_encontrado}
    RETURN    ${valor_encontrado}

Abrir Home Do HOT
    Go To    ${HOT_HOME}
    Wait For Load State    domcontentloaded
    # O log real confirmou que #note_modal intercepta os cliques enquanto estiver aberto.
    ${tem_modal}=    Run Keyword And Return Status    Wait For Elements State    ${LOC_MODAL_AVISO}    visible    timeout=2s
    IF    ${tem_modal}
        Wait For Elements State    ${LOC_AVISO_OK}    visible
        Click    ${LOC_AVISO_OK}
        Wait For Elements State    ${LOC_MODAL_AVISO}    hidden
    END

Abrir Controle De Inventário
    # O Codegen real registrou Toggle navigation -> Infra -> Controle de Inventário.
    ${toggle_visivel}=    Run Keyword And Return Status    Wait For Elements State    ${LOC_TOGGLE_NAVIGATION}    visible    timeout=2s
    IF    ${toggle_visivel}
        Click    ${LOC_TOGGLE_NAVIGATION}
    END
    Wait For Elements State    ${LOC_MENU_INFRA}    visible
    Click    ${LOC_MENU_INFRA}
    Wait For Elements State    ${LOC_CONTROLE_INVENTARIO}    visible
    Click    ${LOC_CONTROLE_INVENTARIO}
    Wait For Load State    domcontentloaded

Abrir Novo Inventário Em Popup
    [Documentation]    O Codegen comprovou que NOVO abre uma nova Page. Switch Page NEW é o mecanismo oficial da Browser Library para assumir o popup recém-aberto.
    Wait For Elements State    ${LOC_NOVO_INVENTARIO}    visible
    Click    ${LOC_NOVO_INVENTARIO}
    ${pagina_anterior}=    Switch Page    NEW
    Wait For Load State    domcontentloaded

Cadastrar Primeira Nota Fiscal Com Tipo Preenchido
    [Documentation]    Seleciona uma Nota Fiscal existente cujo Tipo seja preenchido automaticamente pelo HOT. Aguarda a atualização real do combo Tipo antes de decidir se a NF é válida.
    Wait For Elements State    ${LOC_ACCORDION_NOTA_FISCAL}    visible    timeout=30s
    Click    ${LOC_ACCORDION_NOTA_FISCAL}
    Wait For Elements State    ${LOC_NOTA_FISCAL}    visible    timeout=30s

    ${opcoes_nf}=    Get Select Options    ${LOC_NOTA_FISCAL}
    ${nf_encontrada}=    Set Variable    ${False}

    FOR    ${opcao_nf}    IN    @{opcoes_nf}
        ${valor_nf}=    Set Variable    ${opcao_nf}[value]
        ${label_nf}=    Set Variable    ${opcao_nf}[label]
        IF    '${valor_nf}' == ''    CONTINUE

        Log    Tentando Nota Fiscal: ${label_nf} | value=${valor_nf}
        Select Options By    ${LOC_NOTA_FISCAL}    value    ${valor_nf}
        Wait For Elements State    ${LOC_TIPO_NOTA_FISCAL}    attached    timeout=30s

        ${tipo_preenchido}=    Set Variable    ${False}
        ${tipo_selecionado}=    Set Variable    ${EMPTY}

        FOR    ${tentativa}    IN RANGE    1    11
            ${opcoes_tipo}=    Get Select Options    ${LOC_TIPO_NOTA_FISCAL}
            FOR    ${opcao_tipo}    IN    @{opcoes_tipo}
                ${selecionada}=    Set Variable    ${opcao_tipo}[selected]
                ${valor_tipo}=    Set Variable    ${opcao_tipo}[value]
                ${label_tipo}=    Set Variable    ${opcao_tipo}[label]
                IF    ${selecionada} and '${valor_tipo}' != ''
                    ${tipo_preenchido}=    Set Variable    ${True}
                    ${tipo_selecionado}=    Set Variable    ${label_tipo}
                    BREAK
                END
            END

            IF    ${tipo_preenchido}
                BREAK
            END

            Sleep    500ms
        END

        IF    ${tipo_preenchido}
            Log    Nota Fiscal válida encontrada: ${label_nf} | Tipo=${tipo_selecionado}
            ${nf_encontrada}=    Set Variable    ${True}
            BREAK
        ELSE
            Log    Nota Fiscal sem Tipo preenchido após aguardar atualização: ${label_nf}
        END
    END

    Should Be True    ${nf_encontrada}    Nenhuma Nota Fiscal disponível apresentou Tipo preenchido após aguardar a atualização do HOT.
    Wait For Elements State    ${LOC_SALVAR}    visible    timeout=30s
    Wait For Elements State    ${LOC_SALVAR}    enabled    timeout=30s
    Click    ${LOC_SALVAR}
    Wait For Load State    domcontentloaded
    Validar Status Em Cadastro

Preencher Localização Confirmada Pelo Codegen
    [Arguments]    ${localizacao}
    Click    ${LOC_ACCORDION_LOCALIZACAO}
    Selecionar Opção Disponível Pelo Texto    ${LOC_ORIGEM}    ${localizacao}
    Fill Text    ${LOC_LOCALIZACAO_ATIVO}    ${localizacao}
    Press Keys    ${LOC_LOCALIZACAO_ATIVO}    Tab
    Selecionar Opção Disponível Pelo Texto    ${LOC_ESTADO}    ${localizacao}
    Click    ${LOC_SALVAR}
    Wait For Load State    domcontentloaded
    Validar Status Em Cadastro

Preencher Configuração Confirmada Pelo Codegen
    [Documentation]    Todos os combos genéricos de configuração usam a primeira opção válida disponível no momento da execução.
    Wait For Elements State    ${LOC_ACCORDION_CONFIGURACOES}    visible    timeout=30s
    Click    ${LOC_ACCORDION_CONFIGURACOES}
    Selecionar Primeira Opção Disponível    ${LOC_TIPO_EQUIPAMENTO}
    Selecionar Primeira Opção Disponível    ${LOC_IMAGEM}
    Selecionar Primeira Opção Disponível    ${LOC_FABRICANTE}
    Selecionar Primeira Opção Disponível    ${LOC_MODELO}
    Selecionar Primeira Opção Disponível    ${LOC_PROCESSADOR}
    Selecionar Primeira Opção Disponível    ${LOC_GERACAO_PROCESSADOR}
    Selecionar Primeira Opção Disponível    ${LOC_MEMORIA}
    Selecionar Primeira Opção Disponível    ${LOC_ARMAZENAMENTO}
    Selecionar Primeira Opção Disponível    ${LOC_CAPACIDADE_ARMAZENAMENTO}
    Click    ${LOC_SALVAR}
    Wait For Load State    domcontentloaded

Incluir Ativo Confirmado Pelo Codegen
    [Arguments]    ${armario}    ${numero_ativo}    ${serial}
    Click    ${LOC_ACCORDION_DOCUMENTOS}
    Click    ${LOC_ACCORDION_INCLUSAO_ATIVOS}
    Fill Text    ${LOC_ARMARIO}         ${armario}
    Fill Text    ${LOC_NUMERO_ATIVO}    ${numero_ativo}
    Fill Text    ${LOC_SERIAL}          ${serial}
    Log    Inclusão usando serial: ${serial}
    Log    Inclusão usando número do ativo: ${numero_ativo}
    Registrar Evidencia    05_campos_ativo_preenchidos
    Click    ${LOC_ADICIONAR}
    Registrar Evidencia    06_apos_clicar_adicionar
    Wait For Elements State    ${LOC_DETALHES_ATIVOS}    visible    timeout=30s
    Click    ${LOC_DETALHES_ATIVOS}
    Registrar Evidencia    07_detalhes_ativo_abertos
    Get Text    body    contains    ${serial}
    Get Text    body    contains    ${numero_ativo}
    Click    ${LOC_SALVAR}
    Wait For Load State    domcontentloaded

Pesquisar E Abrir Ativo Confirmado Pelo Codegen
    [Arguments]    ${serial}    ${numero_ativo}
    Log    Pesquisa obrigatoriamente usando o mesmo serial cadastrado: ${serial}
    Wait For Elements State    ${LOC_PESQUISA}    visible    timeout=30s
    Registrar Evidencia    09_lista_antes_pesquisa_serial
    Click    ${LOC_PESQUISA}
    Type Text    ${LOC_PESQUISA}    ${serial}    delay=150ms
    Registrar Evidencia    10_pesquisa_pelo_serial_preenchida
    Wait For Elements State    role=columnheader[name="${numero_ativo}"]    visible    timeout=30s
    Registrar Evidencia    11_resultado_encontrado_pelo_serial
    Click    role=columnheader[name="${numero_ativo}"]
    Wait For Load State    domcontentloaded

Validar Status Em Cadastro
    [Documentation]    Aguarda a página concluir o salvamento e exibir o status confirmado pelo Codegen.
    Wait For Elements State    ${LOC_STATUS_EM_CADASTRO}    visible    timeout=30s
    Wait For Elements State    ${LOC_EQUIPAMENTO_FUNCIONAL}    visible    timeout=30s

Validar Ativo Em Estoque E Funcional
    Wait For Elements State    ${LOC_STATUS_EM_ESTOQUE}    visible    timeout=30s
    Wait For Elements State    ${LOC_EQUIPAMENTO_FUNCIONAL}    visible    timeout=30s
