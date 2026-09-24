*** Settings ***
Documentation    Keywords de negócio DEF-001 reconstruídos a partir do Codegen. Pontos ambíguos param explicitamente em vez de usar suposições.
Resource         ../../../pages/hot/inventario_page.resource
Resource         ../../../pages/hot/defeito_page.resource

*** Keywords ***
Iniciar Declaração De Defeito
    [Documentation]    Não associa Projeto/Funcionário. Abre Mais Opções > Ações.
    Abrir Ação De Alteração De Status

Declarar Defeito Confirmado Pelo Codegen
    [Arguments]    ${massa}    ${laudo_hitss}
    Declarar Defeito Depois Que Ação Estiver Aberta
    ...    2
    ...    ${massa}[chamado_hitss]
    ...    ${laudo_hitss}
    ...    Bateria Estufada
    ...    Defeito Aberto

Preencher Dados De Manutenção Confirmados
    [Arguments]    ${massa}    ${laudo_fornecedor}
    Preencher Manutenção Confirmada Pelo Codegen
    ...    Positivo
    ...    ${massa}[chamado_fornecedor]
    ...    ${laudo_fornecedor}

Informar Equipamento Dentro Da Garantia
    Informar Garantia E Salvar    true

Informar Que A Peça Está Disponível
    Informar Peca Disponivel E Salvar    true

Retornar Equipamento Ao Estoque
    Abrir Ação De Alteração De Status
    Registrar Evidencia    23_mais_opcoes_final_aberto
    Registrar Evidencia    24_painel_acoes_final_aberto
    Retornar Ao Estoque Depois Que Ação Estiver Aberta
    ...    3
    ...    Ativo disponível para uso.

Informar Equipamento Dentro Da Garantia Com Peca
    [Documentation]    DEF-002: dentro da garantia e com peça disponível, sem passar por AGUARDANDO PEÇA.
    Informar Garantia Com Peca E Salvar

Informar Equipamento Fora Da Garantia Com Reparo Aprovado
    [Arguments]    ${massa}    ${orcamento_pdf}
    Informar Fora Da Garantia Com Reparo Aprovado E Salvar
    ...    ${orcamento_pdf}
    ...    ${massa}[numero_pedido]
    ...    ${massa}[remessa_reparo]

Informar Equipamento Fora Da Garantia Com Reparo Reprovado Maquina Funcional
    [Arguments]    ${orcamento_pdf}
    Informar Fora Da Garantia Com Reparo Reprovado Maquina Funcional E Salvar
    ...    ${orcamento_pdf}

Informar Equipamento Fora Da Garantia Com Reparo Reprovado Maquina Nao Funcional
    [Arguments]    ${orcamento_pdf}
    Informar Fora Da Garantia Com Reparo Reprovado Maquina Nao Funcional E Salvar
    ...    ${orcamento_pdf}
