CHECKS = {
    "HOT-INV-DEF-001": {
        "name": "Defeito Dentro da Garantia e Sem Peça",
        "checks": [
            ("CHK-001","Nota Fiscal válida e status inicial","Cadastrar Primeira Nota Fiscal Com Tipo Preenchido","Nota Fiscal possui Tipo preenchido e, após salvar, o ativo permanece EM CADASTRO / Equipamento Funcional.",["02_nota_fiscal_salva.png"]),
            ("CHK-002","Localização salva","Preencher Localização Confirmada Pelo Codegen","Após salvar a localização, o ativo permanece EM CADASTRO / Equipamento Funcional.",["03_localizacao_salva.png"]),
            ("CHK-003","Configurações disponíveis","Preencher Configuração Confirmada Pelo Codegen","A seção de Configurações está disponível e o preenchimento/salvamento é concluído sem erro.",["04_configuracoes_salvas.png"]),
            ("CHK-004","Detalhes do ativo disponíveis","Incluir Ativo Confirmado Pelo Codegen","Após adicionar o ativo, a seção Detalhes dos Números de Ativo/Serial é exibida.",["06_apos_clicar_adicionar.png","07_detalhes_ativo_abertos.png"]),
            ("CHK-005","Serial incluído confere","Incluir Ativo Confirmado Pelo Codegen","O mesmo Serial gerado para o cenário é encontrado nos detalhes do ativo.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-006","Número do ativo incluído confere","Incluir Ativo Confirmado Pelo Codegen","O mesmo Número do Ativo gerado para o cenário é encontrado nos detalhes.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-007","Busca encontra o ativo","Pesquisar E Abrir Ativo Confirmado Pelo Codegen","A pesquisa pelo mesmo Serial retorna o Número do Ativo esperado.",["10_pesquisa_pelo_serial_preenchida.png","11_resultado_encontrado_pelo_serial.png"]),
            ("CHK-008","Ativo inicial em estoque e funcional","Validar Ativo Em Estoque E Funcional","Ao abrir o ativo, exibe STATUS: EM ESTOQUE e Equipamento Funcional.",["13_ativo_em_estoque_funcional.png"]),
            ("CHK-009","Status alterado para defeito","Validar Status Defeito","Após declarar o defeito, exibe STATUS: DEFEITO e Equipamento com Defeito.",["17_status_defeito.png"]),
            ("CHK-010","Sem peça: aguardando peça","Validar Aguardando Peca","Garantia = Sim e sem peça resulta em STATUS: AGUARDANDO PECA / Equipamento com Defeito.",["20_status_aguardando_peca.png"]),
            ("CHK-011","Peça disponível: aguardando reparo","Validar Aguardando Reparo","Após informar peça disponível, exibe STATUS: AGUARDANDO REPARO / Equipamento com Defeito.",["22_status_aguardando_reparo.png"]),
            ("CHK-012","Retorno final ao estoque","Validar Retorno Ao Estoque","Após o reparo, exibe STATUS: EM ESTOQUE / Equipamento Funcional.",["26_status_final_em_estoque_funcional.png"])
        ]
    },
    "HOT-INV-DEF-002": {
        "name": "Defeito Dentro da Garantia e Com Peça",
        "checks": [
            ("CHK-001","Nota Fiscal válida e status inicial","Cadastrar Primeira Nota Fiscal Com Tipo Preenchido","Nota Fiscal possui Tipo preenchido e, após salvar, o ativo permanece EM CADASTRO / Equipamento Funcional.",["02_nota_fiscal_salva.png"]),
            ("CHK-002","Localização salva","Preencher Localização Confirmada Pelo Codegen","Após salvar a localização, o ativo permanece EM CADASTRO / Equipamento Funcional.",["03_localizacao_salva.png"]),
            ("CHK-003","Configurações disponíveis","Preencher Configuração Confirmada Pelo Codegen","A seção de Configurações está disponível e o preenchimento/salvamento é concluído sem erro.",["04_configuracoes_salvas.png"]),
            ("CHK-004","Detalhes do ativo disponíveis","Incluir Ativo Confirmado Pelo Codegen","Após adicionar o ativo, a seção Detalhes dos Números de Ativo/Serial é exibida.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-005","Serial incluído confere","Incluir Ativo Confirmado Pelo Codegen","O mesmo Serial gerado é encontrado nos detalhes.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-006","Número do ativo incluído confere","Incluir Ativo Confirmado Pelo Codegen","O mesmo Número do Ativo gerado é encontrado nos detalhes.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-007","Busca encontra o ativo","Pesquisar E Abrir Ativo Confirmado Pelo Codegen","A pesquisa pelo mesmo Serial retorna o Número do Ativo esperado.",["11_resultado_encontrado_pelo_serial.png"]),
            ("CHK-008","Ativo inicial em estoque e funcional","Validar Ativo Em Estoque E Funcional","Ao abrir o ativo, exibe STATUS: EM ESTOQUE e Equipamento Funcional.",["13_ativo_em_estoque_funcional.png"]),
            ("CHK-009","Status alterado para defeito","Validar Status Defeito","Após declarar o defeito, exibe STATUS: DEFEITO e Equipamento com Defeito.",["17_status_defeito.png"]),
            ("CHK-010","Com peça: aguardando reparo","Validar Aguardando Reparo","Garantia = Sim e Tem peça = Sim resulta diretamente em STATUS: AGUARDANDO REPARO / Equipamento com Defeito.",["22_status_aguardando_reparo.png"]),
            ("CHK-011","Retorno final ao estoque","Validar Retorno Ao Estoque","Após o reparo, exibe STATUS: EM ESTOQUE / Equipamento Funcional.",["26_status_final_em_estoque_funcional.png"])
        ]
    },
    "HOT-INV-DEF-003": {
        "name": "Defeito Fora da Garantia + Reparo Aprovado",
        "checks": [
            ("CHK-001","Nota Fiscal válida e status inicial","Cadastrar Primeira Nota Fiscal Com Tipo Preenchido","Nota Fiscal possui Tipo preenchido e, após salvar, o ativo permanece EM CADASTRO / Equipamento Funcional.",["02_nota_fiscal_salva.png"]),
            ("CHK-002","Localização salva","Preencher Localização Confirmada Pelo Codegen","Após salvar a localização, o ativo permanece EM CADASTRO / Equipamento Funcional.",["03_localizacao_salva.png"]),
            ("CHK-003","Configurações disponíveis","Preencher Configuração Confirmada Pelo Codegen","A seção de Configurações está disponível e o preenchimento/salvamento é concluído sem erro.",["04_configuracoes_salvas.png"]),
            ("CHK-004","Detalhes do ativo disponíveis","Incluir Ativo Confirmado Pelo Codegen","A seção de detalhes é exibida após a inclusão.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-005","Serial incluído confere","Incluir Ativo Confirmado Pelo Codegen","O mesmo Serial gerado é encontrado nos detalhes.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-006","Número do ativo incluído confere","Incluir Ativo Confirmado Pelo Codegen","O mesmo Número do Ativo gerado é encontrado nos detalhes.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-007","Busca encontra o ativo","Pesquisar E Abrir Ativo Confirmado Pelo Codegen","A busca pelo Serial retorna o ativo esperado.",["11_resultado_encontrado_pelo_serial.png"]),
            ("CHK-008","Ativo inicial em estoque e funcional","Validar Ativo Em Estoque E Funcional","Exibe STATUS: EM ESTOQUE / Equipamento Funcional.",["13_ativo_em_estoque_funcional.png"]),
            ("CHK-009","Status alterado para defeito","Validar Status Defeito","Exibe STATUS: DEFEITO / Equipamento com Defeito.",["17_status_defeito.png"]),
            ("CHK-010","Orçamento habilitado fora da garantia","Informar Fora Da Garantia Com Reparo Aprovado E Salvar","Garantia = Não exibe o campo para anexar Orçamento.",["19_fora_da_garantia_orcamento_exibido.png"]),
            ("CHK-011","Reparo aprovado habilitado","Informar Fora Da Garantia Com Reparo Aprovado E Salvar","Após anexar o orçamento, o campo Reparo Aprovado é exibido.",["20_orcamento_anexado_reparo_aprovado_exibido.png"]),
            ("CHK-012","Pedido e remessa habilitados","Informar Fora Da Garantia Com Reparo Aprovado E Salvar","Reparo Aprovado = Sim exibe Número do Pedido e Remessa do Reparo.",["21_reparo_aprovado_campos_pedido_remessa_exibidos.png"]),
            ("CHK-013","Reparo aprovado: aguardando reparo","Validar Aguardando Reparo","Após salvar, exibe STATUS: AGUARDANDO REPARO / Equipamento com Defeito.",["22_status_aguardando_reparo.png"]),
            ("CHK-014","Retorno final ao estoque","Validar Retorno Ao Estoque","Após o reparo, exibe STATUS: EM ESTOQUE / Equipamento Funcional.",["26_status_final_em_estoque_funcional.png"])
        ]
    },
    "HOT-INV-DEF-004": {
        "name": "Defeito Fora da Garantia + Reparo Reprovado + Máquina Funcional",
        "checks": [
            ("CHK-001","Nota Fiscal válida e status inicial","Cadastrar Primeira Nota Fiscal Com Tipo Preenchido","Nota Fiscal possui Tipo preenchido e, após salvar, o ativo permanece EM CADASTRO / Equipamento Funcional.",["02_nota_fiscal_salva.png"]),
            ("CHK-002","Localização salva","Preencher Localização Confirmada Pelo Codegen","Após salvar a localização, o ativo permanece EM CADASTRO / Equipamento Funcional.",["03_localizacao_salva.png"]),
            ("CHK-003","Configurações disponíveis","Preencher Configuração Confirmada Pelo Codegen","A seção de Configurações está disponível e o preenchimento/salvamento é concluído sem erro.",["04_configuracoes_salvas.png"]),
            ("CHK-004","Detalhes do ativo disponíveis","Incluir Ativo Confirmado Pelo Codegen","A seção de detalhes é exibida após a inclusão.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-005","Serial incluído confere","Incluir Ativo Confirmado Pelo Codegen","O mesmo Serial gerado é encontrado nos detalhes.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-006","Número do ativo incluído confere","Incluir Ativo Confirmado Pelo Codegen","O mesmo Número do Ativo gerado é encontrado nos detalhes.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-007","Busca encontra o ativo","Pesquisar E Abrir Ativo Confirmado Pelo Codegen","A busca pelo Serial retorna o ativo esperado.",["11_resultado_encontrado_pelo_serial.png"]),
            ("CHK-008","Ativo inicial em estoque e funcional","Validar Ativo Em Estoque E Funcional","Exibe STATUS: EM ESTOQUE / Equipamento Funcional.",["13_ativo_em_estoque_funcional.png"]),
            ("CHK-009","Status alterado para defeito","Validar Status Defeito","Exibe STATUS: DEFEITO / Equipamento com Defeito.",["17_status_defeito.png"]),
            ("CHK-010","Orçamento habilitado fora da garantia","Informar Fora Da Garantia Com Reparo Reprovado Maquina Funcional E Salvar","Garantia = Não exibe o campo para anexar Orçamento.",["19_fora_da_garantia_orcamento_exibido.png"]),
            ("CHK-011","Reparo reprovado habilita Estado da máquina","Informar Fora Da Garantia Com Reparo Reprovado Maquina Funcional E Salvar","Após Reparo Aprovado = Não, o campo Estado da máquina é exibido.",["21_reparo_reprovado_estado_maquina_exibido.png"]),
            ("CHK-012","Máquina funcional selecionada","Informar Fora Da Garantia Com Reparo Reprovado Maquina Funcional E Salvar","Estado da máquina = Máquina funcional é selecionado antes do salvamento.",["22_maquina_funcional_antes_salvar.png"]),
            ("CHK-013","Resultado final funcional com defeito","Validar Em Estoque Com Defeito Mas Funcional","Exibe STATUS: EM ESTOQUE / Equipamento com Defeito mas Funcional.",["23_status_final_em_estoque_defeito_funcional.png"])
        ]
    },
    "HOT-INV-DEF-005": {
        "name": "Defeito Fora da Garantia + Reparo Reprovado + Máquina Não Funcional",
        "checks": [
            ("CHK-001","Nota Fiscal válida e status inicial","Cadastrar Primeira Nota Fiscal Com Tipo Preenchido","Nota Fiscal possui Tipo preenchido e, após salvar, o ativo permanece EM CADASTRO / Equipamento Funcional.",["02_nota_fiscal_salva.png"]),
            ("CHK-002","Localização salva","Preencher Localização Confirmada Pelo Codegen","Após salvar a localização, o ativo permanece EM CADASTRO / Equipamento Funcional.",["03_localizacao_salva.png"]),
            ("CHK-003","Configurações disponíveis","Preencher Configuração Confirmada Pelo Codegen","A seção de Configurações está disponível e o preenchimento/salvamento é concluído sem erro.",["04_configuracoes_salvas.png"]),
            ("CHK-004","Detalhes do ativo disponíveis","Incluir Ativo Confirmado Pelo Codegen","A seção de detalhes é exibida após a inclusão.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-005","Serial incluído confere","Incluir Ativo Confirmado Pelo Codegen","O mesmo Serial gerado é encontrado nos detalhes.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-006","Número do ativo incluído confere","Incluir Ativo Confirmado Pelo Codegen","O mesmo Número do Ativo gerado é encontrado nos detalhes.",["07_detalhes_ativo_abertos.png"]),
            ("CHK-007","Busca encontra o ativo","Pesquisar E Abrir Ativo Confirmado Pelo Codegen","A busca pelo Serial retorna o ativo esperado.",["11_resultado_encontrado_pelo_serial.png"]),
            ("CHK-008","Ativo inicial em estoque e funcional","Validar Ativo Em Estoque E Funcional","Exibe STATUS: EM ESTOQUE / Equipamento Funcional.",["13_ativo_em_estoque_funcional.png"]),
            ("CHK-009","Status alterado para defeito","Validar Status Defeito","Exibe STATUS: DEFEITO / Equipamento com Defeito.",["17_status_defeito.png"]),
            ("CHK-010","Orçamento habilitado fora da garantia","Informar Fora Da Garantia Com Reparo Reprovado Maquina Nao Funcional E Salvar","Garantia = Não exibe o campo para anexar Orçamento.",["19_fora_da_garantia_orcamento_exibido.png"]),
            ("CHK-011","Reparo reprovado habilita Estado da máquina","Informar Fora Da Garantia Com Reparo Reprovado Maquina Nao Funcional E Salvar","Após Reparo Aprovado = Não, o campo Estado da máquina é exibido.",["21_reparo_reprovado_estado_maquina_exibido.png"]),
            ("CHK-012","Máquina não funcional selecionada","Informar Fora Da Garantia Com Reparo Reprovado Maquina Nao Funcional E Salvar","Estado da máquina = Máquina não funcional é selecionado antes do salvamento.",["22_maquina_nao_funcional_antes_salvar.png"]),
            ("CHK-013","Resultado final não funcional","Validar Reparo Nao Autorizado Com Defeito Nao Funcional","Exibe STATUS: REPARO NAO AUTORIZADO / Equipamento com Defeito e Não Funcional.",["23_status_final_reparo_nao_autorizado_nao_funcional.png"])
        ]
    }
}
