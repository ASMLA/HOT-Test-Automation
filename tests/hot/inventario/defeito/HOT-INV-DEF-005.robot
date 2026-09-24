*** Settings ***
Documentation    DEF-005 - Defeito Fora Da Garantia + Reparo Reprovado + Máquina Não Funcional.
Resource         ../../../../resources/keywords/technical/browser_keywords.resource
Resource         ../../../../resources/keywords/technical/evidence_keywords.resource
Resource         ../../../../resources/keywords/business/hot/inventario_keywords.resource
Resource         ../../../../resources/keywords/business/hot/defeito_keywords.resource
Suite Setup      Open Browser Session
Test Setup       Preparar Pasta De Evidencias
Test Teardown    Registrar Evidencia Final Do Teste
Suite Teardown   Close Browser Session

*** Variables ***
${LAUDO_HITSS}         ${EXECDIR}/data/fixtures/laudos/laudo_hitss.pdf
${LAUDO_FORNECEDOR}    ${EXECDIR}/data/fixtures/laudos/laudo_fornecedor.pdf
${ORCAMENTO}           ${EXECDIR}/data/fixtures/laudos/Orcamento fora da garantia.pdf

${EVIDENCE_SCENARIO}   HOT-INV-DEF-005
${EVIDENCE_DIR}        ${EVIDENCE_ROOT}${/}${EVIDENCE_SCENARIO}

*** Test Cases ***
HOT-INV-DEF-005 - Defeito Fora Da Garantia Reparo Reprovado Maquina Nao Funcional
    [Tags]    HOT    INVENTARIO    DEFEITO    DEF-005    FORA-GARANTIA    REPARO-REPROVADO    MAQUINA-NAO-FUNCIONAL    E2E

    ${massa}=    Gerar Massa Do Ativo DEF-005
    Log    Serial gerado para toda a execução: ${massa}[serial]
    Log    Número do ativo gerado para toda a execução: ${massa}[numero_ativo]

    Acessar Controle De Inventário
    Registrar Evidencia    01_controle_inventario_aberto

    Cadastrar Nota Fiscal Do Inventário
    Registrar Evidencia    02_nota_fiscal_salva

    Informar Localização Do Equipamento
    Registrar Evidencia    03_localizacao_salva

    Configurar Equipamento Com Valores Confirmados
    Registrar Evidencia    04_configuracoes_salvas

    Incluir Novo Ativo    ${massa}
    Registrar Evidencia    08_ativo_incluido_e_salvo

    Localizar E Abrir Ativo Criado    ${massa}
    Registrar Evidencia    12_ativo_localizado_e_aberto

    Validar Ativo Em Estoque E Funcional
    Registrar Evidencia    13_ativo_em_estoque_funcional

    Iniciar Declaração De Defeito
    Declarar Defeito Confirmado Pelo Codegen    ${massa}    ${LAUDO_HITSS}
    Validar Status Defeito

    Preencher Dados De Manutenção Confirmados    ${massa}    ${LAUDO_FORNECEDOR}
    Informar Equipamento Fora Da Garantia Com Reparo Reprovado Maquina Nao Funcional    ${ORCAMENTO}
    Validar Reparo Nao Autorizado Com Defeito Nao Funcional
