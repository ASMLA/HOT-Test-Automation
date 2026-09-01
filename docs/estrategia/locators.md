# Estratégia de Locators — HOT

Nenhum locator específico do HOT será criado apenas por inferência visual de screenshots.

## Ordem de preferência

1. `data-testid`, `data-test` ou atributo de automação estável
2. `id` estável e sem valor dinâmico
3. `name` estável
4. role + accessible name
5. label associado ao campo
6. texto estável de negócio
7. CSS/XPath estruturado apenas quando as opções anteriores não forem possíveis

## Evitar

- XPath absoluto
- índices como `div[3]`
- classes geradas dinamicamente
- seletores baseados exclusivamente em posição
- sleeps fixos para mascarar sincronização

## Processo de captura

Para cada elemento:

1. abrir o DevTools;
2. selecionar o elemento;
3. registrar o HTML relevante;
4. verificar se o atributo é estável ao recarregar a página;
5. escolher o menor locator robusto;
6. registrar no Page Object;
7. testar a ação isoladamente;
8. somente depois incorporar ao fluxo de negócio.

## Primeiro mapeamento

A captura começa em `Controle de Equipamentos → Cadastro de Estoque → Nota Fiscal` e avança até `AGUARDANDO REPARO` no cenário DEF-002.
