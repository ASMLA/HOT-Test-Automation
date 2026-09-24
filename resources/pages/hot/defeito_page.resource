*** Settings ***
Documentation    Page Object do fluxo de Defeito reconstruído somente com locators comprovados pelo Playwright Codegen.
Library          Browser
Library          BuiltIn
Resource         ../../keywords/technical/evidence_keywords.resource

*** Variables ***
${LOC_MAIS_OPCOES}                  role=button[name="Mais Opções"]
${LOC_ACOES}    css=#actions

# O Codegen confirmou o campo abaixo depois que a ação é aberta.
${LOC_ALTERAR_STATUS}               role=combobox[name="Alterar Status Para"]
${LOC_CHAMADO_HITSS}                role=textbox[name="Chamado HITSS"]
${LOC_LAUDO_HITSS}                  role=button[name="Choose File"]
${LOC_BUSCA_TIPO_DEFEITO}           role=searchbox[name="Search"]
${LOC_COMENTARIO}                   role=textbox[name="Comentário"]

${LOC_DADOS_MANUTENCAO}             role=button[name="Dados de Manutenção"]
${LOC_FORNECEDOR}                   role=combobox[name="Fornecedor"]
${LOC_CHAMADO_FORNECEDOR}           role=textbox[name="Chamado Fornecedor"]
${LOC_LAUDO_FORNECEDOR}             role=button[name="Laudo Fornecedor"]
${LOC_DENTRO_GARANTIA}              role=combobox[name="Está dentro da garantia?"]
${LOC_TEM_PECA}                     role=combobox[name="Tem peça?"]
${LOC_REPARO_APROVADO}              css=#repair_approved
${LOC_ESTADO_MAQUINA}               css=#machine_status
${LOC_ANEXAR_ORCAMENTO}              css=#budget_file
${LOC_NUMERO_PEDIDO}                 css=#order_number
${LOC_REMESSA_REPARO}                css=#repair_shipment
${LOC_SALVAR_INVENTARIO}             css=#save_inventory
${LOC_SALVAR}                       role=button[name="Salvar"]
${LOC_SALVAR_ACAO}                  css=#save_action

${TXT_STATUS_DEFEITO}               STATUS: DEFEITO
${TXT_STATUS_AGUARDANDO_PECA}       STATUS: AGUARDANDO PECA
${TXT_STATUS_AGUARDANDO_REPARO}     STATUS: AGUARDANDO REPARO
${TXT_STATUS_ESTOQUE}               STATUS: EM ESTOQUE
${TXT_STATUS_REPARO_NAO_AUTORIZADO}    STATUS: REPARO NAO AUTORIZADO
${TXT_EQUIPAMENTO_DEFEITO}          Equipamento com Defeito
${TXT_EQUIPAMENTO_FUNCIONAL}        Equipamento Funcional
${TXT_EQUIPAMENTO_DEFEITO_FUNCIONAL}    Equipamento com Defeito mas Funcional
${TXT_EQUIPAMENTO_DEFEITO_NAO_FUNCIONAL}    Equipamento com Defeito e Não Funcional

*** Keywords ***
Parar Em Locator Ainda Não Confirmado
    [Arguments]    ${etapa}
    Fail    Locator ainda não confirmado pelo Codegen/Pick Locator para: ${etapa}. Nenhum locator será inventado.

Abrir Ação De Alteração De Status
    [Documentation]    Abre "Mais Opções" e clica no botão Ações usando o locator confirmado pelo mapeamento.
    Wait For Elements State    ${LOC_MAIS_OPCOES}    visible    timeout=30s
    Click    ${LOC_MAIS_OPCOES}
    Registrar Evidencia    14_mais_opcoes_aberto
    Wait For Elements State    ${LOC_ACOES}    visible    timeout=30s
    Click    ${LOC_ACOES}
    Registrar Evidencia    15_painel_acoes_aberto

Declarar Defeito Depois Que Ação Estiver Aberta
    [Arguments]    ${status_value}    ${chamado_hitss}    ${laudo_hitss}    ${tipo_defeito}    ${comentario}
    Select Options By    ${LOC_ALTERAR_STATUS}    value    ${status_value}
    Fill Text    ${LOC_CHAMADO_HITSS}    ${chamado_hitss}
    Upload File By Selector    ${LOC_LAUDO_HITSS}    ${laudo_hitss}
    Click    ${LOC_BUSCA_TIPO_DEFEITO}
    Click    role=option[name="${tipo_defeito}"]
    Fill Text    ${LOC_COMENTARIO}    ${comentario}
    Registrar Evidencia    16_defeito_preenchido_antes_salvar
    Wait For Elements State    ${LOC_SALVAR_ACAO}    visible    timeout=30s
    Click    ${LOC_SALVAR_ACAO}
    Wait For Load State    domcontentloaded

Validar Status Defeito
    Wait For Elements State    text=${TXT_STATUS_DEFEITO}    visible    timeout=30s
    Wait For Elements State    text=${TXT_EQUIPAMENTO_DEFEITO}    visible    timeout=30s
    Registrar Evidencia    17_status_defeito

Preencher Manutenção Confirmada Pelo Codegen
    [Arguments]    ${fornecedor_value}    ${chamado_fornecedor}    ${laudo_fornecedor}
    Wait For Elements State    ${LOC_DADOS_MANUTENCAO}    visible    timeout=30s
    Click    ${LOC_DADOS_MANUTENCAO}
    Select Options By    ${LOC_FORNECEDOR}    value    ${fornecedor_value}
    Fill Text    ${LOC_CHAMADO_FORNECEDOR}    ${chamado_fornecedor}
    Upload File By Selector    ${LOC_LAUDO_FORNECEDOR}    ${laudo_fornecedor}
    Registrar Evidencia    18_dados_manutencao_preenchidos

Informar Garantia E Salvar
    [Arguments]    ${garantia_value}
    Select Options By    ${LOC_DENTRO_GARANTIA}    value    ${garantia_value}
    Registrar Evidencia    19_garantia_informada_antes_salvar
    Click    ${LOC_SALVAR}
    Wait For Load State    domcontentloaded

Validar Aguardando Peca
    Wait For Elements State    text=${TXT_STATUS_AGUARDANDO_PECA}    visible    timeout=30s
    Wait For Elements State    text=${TXT_EQUIPAMENTO_DEFEITO}    visible    timeout=30s
    Registrar Evidencia    20_status_aguardando_peca

Informar Peca Disponivel E Salvar
    [Arguments]    ${tem_peca_value}
    Wait For Elements State    ${LOC_DADOS_MANUTENCAO}    visible    timeout=30s
    Click    ${LOC_DADOS_MANUTENCAO}
    Select Options By    ${LOC_TEM_PECA}    value    ${tem_peca_value}
    Registrar Evidencia    21_peca_disponivel_antes_salvar
    Click    ${LOC_SALVAR}
    Wait For Load State    domcontentloaded

Validar Aguardando Reparo
    Wait For Elements State    text=${TXT_STATUS_AGUARDANDO_REPARO}    visible    timeout=30s
    Wait For Elements State    text=${TXT_EQUIPAMENTO_DEFEITO}    visible    timeout=30s
    Registrar Evidencia    22_status_aguardando_reparo

Retornar Ao Estoque Depois Que Ação Estiver Aberta
    [Arguments]    ${status_value}    ${comentario}
    Select Options By    ${LOC_ALTERAR_STATUS}    value    ${status_value}
    Fill Text    ${LOC_COMENTARIO}    ${comentario}
    Registrar Evidencia    25_retorno_estoque_preenchido_antes_salvar
    Wait For Elements State    ${LOC_SALVAR_ACAO}    visible    timeout=30s
    Click    ${LOC_SALVAR_ACAO}
    Wait For Load State    domcontentloaded

Validar Retorno Ao Estoque
    Wait For Elements State    text=${TXT_STATUS_ESTOQUE}    visible    timeout=30s
    Wait For Elements State    text=${TXT_EQUIPAMENTO_FUNCIONAL}    visible    timeout=30s
    Registrar Evidencia    26_status_final_em_estoque_funcional

Informar Garantia Com Peca E Salvar
    [Documentation]    DEF-002: usa os mesmos locators já validados no DEF-001. Seleciona garantia Sim e peça Sim antes de salvar.
    Select Options By    ${LOC_DENTRO_GARANTIA}    value    true
    Registrar Evidencia    19_garantia_sim
    Wait For Elements State    ${LOC_TEM_PECA}    visible    timeout=30s
    Select Options By    ${LOC_TEM_PECA}    value    true
    Registrar Evidencia    20_peca_sim_antes_salvar
    Click    ${LOC_SALVAR}
    Wait For Load State    domcontentloaded

Informar Fora Da Garantia Com Reparo Aprovado E Salvar
    [Arguments]    ${orcamento_pdf}    ${numero_pedido}    ${remessa_reparo}
    [Documentation]    Fluxo confirmado manualmente para DEF-003: Garantia Não -> Orçamento -> Reparo Aprovado Sim -> Pedido + Remessa -> Salvar.
    Select Options By    ${LOC_DENTRO_GARANTIA}    value    false
    Wait For Elements State    ${LOC_ANEXAR_ORCAMENTO}    visible    timeout=30s
    Registrar Evidencia    19_fora_da_garantia_orcamento_exibido

    Upload File By Selector    ${LOC_ANEXAR_ORCAMENTO}    ${orcamento_pdf}
    Wait For Elements State    ${LOC_REPARO_APROVADO}    visible    timeout=30s
    Registrar Evidencia    20_orcamento_anexado_reparo_aprovado_exibido

    Select Options By    ${LOC_REPARO_APROVADO}    value    true
    Wait For Elements State    ${LOC_NUMERO_PEDIDO}    visible    timeout=30s
    Wait For Elements State    ${LOC_REMESSA_REPARO}    visible    timeout=30s
    Registrar Evidencia    21_reparo_aprovado_campos_pedido_remessa_exibidos

    Fill Text    ${LOC_NUMERO_PEDIDO}    ${numero_pedido}
    Fill Text    ${LOC_REMESSA_REPARO}    ${remessa_reparo}
    Registrar Evidencia    22_pedido_e_remessa_preenchidos_antes_salvar

    Wait For Elements State    ${LOC_SALVAR_INVENTARIO}    visible    timeout=30s
    Click    ${LOC_SALVAR_INVENTARIO}
    Wait For Load State    domcontentloaded

Informar Fora Da Garantia Com Reparo Reprovado Maquina Funcional E Salvar
    [Arguments]    ${orcamento_pdf}
    [Documentation]    DEF-004 confirmado: Garantia Não -> anexar Orçamento -> Reparo Aprovado Não -> Estado da máquina funcional -> Salvar.
    Select Options By    ${LOC_DENTRO_GARANTIA}    value    false
    Wait For Elements State    ${LOC_ANEXAR_ORCAMENTO}    visible    timeout=30s
    Registrar Evidencia    19_fora_da_garantia_orcamento_exibido

    Upload File By Selector    ${LOC_ANEXAR_ORCAMENTO}    ${orcamento_pdf}
    Wait For Elements State    ${LOC_REPARO_APROVADO}    visible    timeout=30s
    Registrar Evidencia    20_orcamento_anexado_reparo_aprovado_exibido

    Select Options By    ${LOC_REPARO_APROVADO}    value    false
    Wait For Elements State    ${LOC_ESTADO_MAQUINA}    visible    timeout=30s
    Registrar Evidencia    21_reparo_reprovado_estado_maquina_exibido

    Select Options By    ${LOC_ESTADO_MAQUINA}    value    true
    Registrar Evidencia    22_maquina_funcional_antes_salvar

    Wait For Elements State    ${LOC_SALVAR_INVENTARIO}    visible    timeout=30s
    Click    ${LOC_SALVAR_INVENTARIO}
    Wait For Load State    domcontentloaded

Validar Em Estoque Com Defeito Mas Funcional
    Wait For Elements State    text=${TXT_STATUS_ESTOQUE}    visible    timeout=30s
    Wait For Elements State    text=${TXT_EQUIPAMENTO_DEFEITO_FUNCIONAL}    visible    timeout=30s
    Registrar Evidencia    23_status_final_em_estoque_defeito_funcional

Informar Fora Da Garantia Com Reparo Reprovado Maquina Nao Funcional E Salvar
    [Arguments]    ${orcamento_pdf}
    [Documentation]    DEF-005 confirmado: Garantia Não -> anexar Orçamento -> Reparo Aprovado Não -> Estado da máquina não funcional -> Salvar.
    Select Options By    ${LOC_DENTRO_GARANTIA}    value    false
    Wait For Elements State    ${LOC_ANEXAR_ORCAMENTO}    visible    timeout=30s
    Registrar Evidencia    19_fora_da_garantia_orcamento_exibido

    Upload File By Selector    ${LOC_ANEXAR_ORCAMENTO}    ${orcamento_pdf}
    Wait For Elements State    ${LOC_REPARO_APROVADO}    visible    timeout=30s
    Registrar Evidencia    20_orcamento_anexado_reparo_aprovado_exibido

    Select Options By    ${LOC_REPARO_APROVADO}    value    false
    Wait For Elements State    ${LOC_ESTADO_MAQUINA}    visible    timeout=30s
    Registrar Evidencia    21_reparo_reprovado_estado_maquina_exibido

    Select Options By    ${LOC_ESTADO_MAQUINA}    value    false
    Registrar Evidencia    22_maquina_nao_funcional_antes_salvar

    Wait For Elements State    ${LOC_SALVAR_INVENTARIO}    visible    timeout=30s
    Click    ${LOC_SALVAR_INVENTARIO}
    Wait For Load State    domcontentloaded

Validar Reparo Nao Autorizado Com Defeito Nao Funcional
    Wait For Elements State    text=${TXT_STATUS_REPARO_NAO_AUTORIZADO}    visible    timeout=30s
    Wait For Elements State    text=${TXT_EQUIPAMENTO_DEFEITO_NAO_FUNCIONAL}    visible    timeout=30s
    Registrar Evidencia    23_status_final_reparo_nao_autorizado_nao_funcional
