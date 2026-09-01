# Visão Geral da Arquitetura — HOT

O projeto HOT utiliza como base as capacidades técnicas consolidadas no Automation Diary Framework v0.24.0, porém possui ciclo de vida, versionamento, documentação e implementação próprios.

## Regra principal

O framework-base não deve receber código específico do HOT. Toda regra de negócio, locator, Page Object, massa e cenário da aplicação pertence exclusivamente a este repositório.

## Camadas

```text
Testes
  ↓
Keywords de Negócio
  ↓
Page Objects
  ↓
Keywords Técnicas
  ↓
Browser / API
  ↓
HOT
```

### Testes

Expressam a regra de negócio e as decisões do cenário. Devem ser pequenos e legíveis.

### Keywords de Negócio

Orquestram ações do domínio, por exemplo:

- Criar Inventário Sem Funcionário
- Declarar Defeito do Ativo
- Informar Dados do Fornecedor
- Informar Situação de Garantia
- Validar Status Completo do Ativo

### Page Objects

Conhecem a interface e os locators. Não devem conter regra de negócio.

### Capacidades Técnicas

Concentram browser, sincronização, configuração, secrets, dados, logs, evidências e observabilidade.

## Regra para status compostos

Nos fluxos DEF-004 e DEF-005, o HOT apresenta o status visualmente em duas linhas, mas o domínio trata a combinação como um único status de negócio. A automação deverá validar o componente completo, sem criar dois estados independentes.
