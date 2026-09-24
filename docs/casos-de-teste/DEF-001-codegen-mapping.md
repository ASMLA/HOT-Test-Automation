# DEF-001 — Reconstrução baseada no Playwright Codegen

## Regra

Este pacote não inventa locators. Só foram implementados elementos que aparecem de forma identificável no Codegen fornecido.

## Descoberta estrutural crítica

O clique em `NOVO` abre uma nova Page/popup. A automação anterior continuava na página original. O pacote corrige isso usando:

```robot
Click    ${LOC_NOVO_INVENTARIO}
${pagina_anterior}=    Switch Page    NEW
```

`Switch Page NEW` é o mecanismo da Browser Library para mudar para o popup recém-aberto.

## Locators confirmados e usados

- `role=button[name="Nota Fiscal"]`
- `css=#invoice`
- `role=button[name="Localização do Equipamento"]`
- `css=#branch`
- `role=textbox[name="Localização Atual do Ativo"]`
- `css=#state`
- `role=button[name="Configurações do Equipamento"]`
- `css=#type_equipment`
- `css=#image`
- `css=#maker`
- `css=#model`
- `css=#processador`
- `css=#processador_generation`
- `css=#memory`
- `css=#storage`
- `css=#storage_capacity`
- `role=button[name="Inclusão dos Ativos"]`
- `role=textbox[name="Armário Armário"]`
- `role=textbox[name="Número do Ativo"]`
- `role=textbox[name="Serial da Máquina"]`
- `role=button[name="Adicionar"]`
- `role=textbox[name="Pesquise Por: ID, Nº Ativo, N"]`
- `role=button[name="Mais Opções"]`
- `label=Alterar Status Para`
- `role=textbox[name="Chamado HITSS"]`
- `role=searchbox[name="Search"]`
- `role=option[name="Touch Pad Quebrado"]`
- `role=textbox[name="Comentário"]`
- `role=button[name="Dados de Manutenção"]`
- `label=Fornecedor`
- `role=textbox[name="Chamado Fornecedor"]`
- `role=button[name="Laudo Fornecedor"]`
- `label=Está dentro da garantia?`
- `label=Tem peça?`

## Pontos ainda não confirmados

O Codegen registrou alguns elementos como:

```python
get_by_label("", exact=True)
```

Isso não identifica semanticamente o controle. Por decisão de projeto, eles NÃO foram substituídos por IDs ou CSS presumidos.

Falta confirmar:

1. o botão/controle exibido após `Mais Opções` que abre o painel de Ação;
2. o botão `Salvar` escopado dentro desse painel de Ação.

Quando esses dois elementos forem obtidos via Pick Locator ou HTML, o fluxo pode ser ligado do `EM ESTOQUE` até `DEFEITO`, `AGUARDANDO PECA`, `AGUARDANDO REPARO` e retorno a `EM ESTOQUE`.

## Correção Browser Library

A versão anterior continha `Wait Until Element Is Visible`, que é um keyword típico de SeleniumLibrary e não existe na Browser Library.

Foi substituído por:

```robot
Wait For Elements State    ${locator}    visible
```

ou, quando há timeout específico:

```robot
Wait For Elements State    ${locator}    visible    timeout=2s
```

Nenhum locator do Codegen foi alterado nesta correção.

## Evidência real — modal da Home

A execução real confirmou que o bloqueio do menu não era o `Toggle navigation`.
O Playwright encontrou o botão corretamente, mas registrou que este elemento interceptava os cliques:

```html
<div id="note_modal" role="dialog" class="modal fade show">
```

Portanto, o modal foi tratado pelo ID comprovado `#note_modal`, e o clique em `OK`
ficou escopado dentro dele. Depois do clique, a automação aguarda o modal ficar
`hidden` antes de tentar abrir o menu.

## Evidência real — sincronização após Salvar

A execução real confirmou que a Nota Fiscal foi localizada, selecionada e salva.
A falha ocorreu porque a validação de `STATUS: EM CADASTRO` foi executada enquanto
a tela ainda exibia o formulário de Cadastro de Estoque.

A validação foi alterada para aguardar explicitamente os textos que o Codegen
confirmou na tela seguinte:

```robot
Wait For Elements State    text=STATUS: EM CADASTRO    visible    timeout=30s
Wait For Elements State    text=Equipamento Funcional    visible    timeout=30s
```

Não foi adicionado `Sleep`; a sincronização espera a condição real da aplicação.

## Evidência real — tecla Tab

O Codegen original registrou:

```python
page1.get_by_role("textbox", name="Localização Atual do Ativo").press("Tab")
```

A implementação anterior converteu incorretamente para `TAB`, e a Browser Library/Playwright
retornou `Unknown key: "TAB"`.

Foi corrigido exatamente para:

```robot
Press Keys    ${LOC_LOCALIZACAO_ATIVO}    Tab
```

Nenhum locator ou dado de negócio foi alterado.

## Evidência real — Detalhes dos Números de Ativo/Serial

A execução parou procurando:

```text
role=button[name="Detalhes dos Números de Ativo"]
```

O mapeamento da tela confirma que o texto e o accessible name completos do botão são:

```text
Detalhes dos Números de Ativo/Serial
```

O próprio mapper marcou esse texto como único na tela.

Por isso o locator foi corrigido para o texto completo confirmado:

```robot
text="Detalhes dos Números de Ativo/Serial"
```

Após `Adicionar`, a automação também aguarda esse botão ficar visível antes do clique.
Nenhum outro locator foi alterado.
