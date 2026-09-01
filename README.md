# HOT Test Automation

Projeto de automação de testes da aplicação **HOT**, criado a partir do baseline arquitetural do **Automation Diary Framework v0.24.0**.

Este é um **projeto independente**. O Automation Diary Framework permanece encerrado em `v0.24.0` e serve aqui apenas como fundação arquitetural e técnica. Toda implementação específica do HOT — regras de negócio, locators, Page Objects, massas e cenários — pertence a este repositório.

## Status do projeto

- Versão inicial: **v0.1.0**
- Aplicação: **HOT Web**
- Módulo inicial: **Controle de Equipamentos / Cadastro de Estoque**
- Primeiro domínio: **Fluxo de Defeito de Inventário**
- Cenários funcionais mapeados: **6 variações**
- Etapa atual: **baseline técnico, instalação local, Git/CI e preparação para captura dos locators reais**

## Objetivo

Criar uma suíte de automação real, reutilizável e sustentável para o HOT, aproveitando as capacidades consolidadas no framework-base:

- Robot Framework;
- Browser Library / Playwright;
- Page Objects;
- Keywords de negócio;
- configuração por ambiente;
- gerenciamento seguro de segredos;
- massa de dados dinâmica;
- registro e cleanup da massa criada;
- sincronização e redução de flakiness;
- logs e evidências;
- relatórios e observabilidade;
- execução paralela;
- integração com CI/CD;
- suporte a APIs quando necessário;
- possibilidade de expansão futura para outros tipos de automação.

## Idioma e padrão de escrita

A documentação, os comentários, os nomes dos cenários e as **keywords de negócio específicas do HOT** são escritos em **português**, facilitando leitura e manutenção pela equipe brasileira.

Nomes internos de bibliotecas, tecnologias e alguns componentes técnicos podem permanecer em inglês quando isso representar o nome oficial da ferramenta ou evitar alteração desnecessária da base técnica.

---

# Arquitetura

A solução segue uma arquitetura em camadas. O teste descreve o comportamento de negócio; os detalhes técnicos ficam nas camadas inferiores.

```text
Testes HOT
    ↓
Keywords de Negócio
    ↓
Page Objects HOT
    ↓
Keywords / Capacidades Técnicas
    ↓
Browser Library / API
    ↓
Aplicação HOT
```

### Testes

Contêm os cenários de negócio e suas validações. Devem ser pequenos, legíveis e evitar detalhes técnicos da interface.

Exemplo conceitual:

```robot
*** Test Cases ***
Criar Inventário Com Defeito Dentro Da Garantia E Com Peça
    Criar Inventário Sem Funcionário
    Declarar Defeito Do Ativo
    Informar Situação Da Garantia    Sim
    Informar Disponibilidade De Peça    Sim
    Validar Status Completo Do Ativo    AGUARDANDO REPARO
```

### Keywords de Negócio

Orquestram o fluxo funcional do HOT, por exemplo:

- Criar Inventário Sem Funcionário;
- Declarar Defeito do Ativo;
- Informar Dados do Fornecedor;
- Informar Situação de Garantia;
- Informar Disponibilidade de Peça;
- Validar Status Completo do Ativo.

### Page Objects

Centralizam os elementos e ações da interface do HOT. Os locators reais são incluídos somente depois de inspecionados e validados no DOM da aplicação.

Os Page Objects **não devem conter regra de negócio**.

### Capacidades técnicas

Concentram recursos reutilizáveis, como:

- abertura e fechamento do navegador;
- sincronização;
- configuração;
- secrets;
- geração e validação de dados;
- cleanup;
- logging;
- métricas;
- evidências;
- observabilidade;
- execução paralela.

Mais detalhes: `docs/arquitetura/visao-geral.md`.

---

# Estrutura do projeto

```text
HOT-Test-Automation/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── ambientes/
│   │   └── hml.yaml
│   ├── fixtures/
│   │   └── laudos/
│   └── hot/
│       └── inventario.yaml
├── docs/
│   ├── arquitetura/
│   ├── casos-de-teste/
│   └── estrategia/
├── reports/
├── resources/
│   ├── api/
│   ├── data/
│   │   ├── builders/
│   │   ├── cleanup/
│   │   ├── generators/
│   │   └── validators/
│   ├── keywords/
│   │   ├── business/hot/
│   │   ├── common/
│   │   └── technical/
│   ├── pages/
│   │   ├── common/
│   │   └── hot/
│   └── variables/
├── scripts/
├── tests/
│   └── hot/
│       └── inventario/
│           └── defeito/
├── requirements.txt
├── CHANGELOG.md
└── README.md
```

## O que fica em cada pasta

| Pasta | Responsabilidade |
|---|---|
| `tests/` | Cenários automatizados do HOT |
| `resources/keywords/business/` | Fluxos e ações de negócio reutilizáveis |
| `resources/pages/` | Page Objects e locators da aplicação |
| `resources/keywords/technical/` | Capacidades técnicas reutilizáveis |
| `resources/data/` | Geração, validação, builders e cleanup de massa |
| `resources/variables/` | Variáveis técnicas e de ambiente |
| `data/ambientes/` | Configurações por ambiente |
| `data/hot/` | Massa e contratos de dados específicos do HOT |
| `data/fixtures/` | Arquivos utilizados nos testes, como laudos |
| `docs/` | Arquitetura, estratégia e especificações funcionais |
| `reports/` | Saída local das execuções |
| `scripts/` | Atalhos para preparação e execução |
| `.github/workflows/` | Pipeline de CI/CD |

---

# Início rápido — preparando uma máquina do zero

Esta seção é o ponto de partida para qualquer pessoa que esteja configurando o projeto pela primeira vez. O objetivo é sair de uma máquina sem o projeto configurado até um ambiente local validado e pronto para executar Robot Framework + Browser Library/Playwright.

## 1. Pré-requisitos

O ambiente de referência validado para o projeto utiliza:

| Ferramenta | Versão de referência | Finalidade |
|---|---:|---|
| Python | **3.12.x** | Runtime do Robot Framework |
| pip | versão compatível com Python 3.12 | Instalação das dependências Python |
| Node.js | **24.x** ou LTS compatível | Dependência técnica utilizada pelo Browser Library/Playwright |
| npm | instalado junto com Node.js | Dependências Node utilizadas pelo Browser Library |
| Git | versão atual estável | Controle de versão |
| Robot Framework | **7.4.2** | Framework de automação |
| Browser Library | **20.2.0** | Automação Web |
| Playwright | **1.62.0** requerido pelo Browser Library 20.2.0 | Engine de automação do navegador |

> O projeto deve utilizar **Python 3.12** na `.venv`. Caso existam várias versões do Python instaladas na máquina, não confie apenas no comando `python --version`; valide também o executável usado pela `.venv`.

### Validação inicial das ferramentas

No Windows, com o terminal aberto na pasta do projeto, execute em uma única linha:

```bat
python --version && where python && where pip && node --version && npm --version && git --version
```

O comando permite identificar não apenas as versões, mas também se existem múltiplas instalações de Python/pip no `PATH`.

## 2. Clonar ou acessar o projeto

Depois que o repositório estiver publicado no GitHub:

```bat
git clone <URL_DO_REPOSITORIO> && cd HOT-Test-Automation
```

Se o projeto já estiver disponível localmente, apenas acesse a pasta:

```bat
cd C:\HOT-Test-Automation
```

## 3. Criar o ambiente virtual com Python 3.12

### Cenário simples — Python 3.12 é o `python` padrão

```bat
python -m venv .venv && .venv\Scripts\activate && python --version
```

O resultado deve indicar `Python 3.12.x`.

### Cenário com mais de uma versão do Python instalada

Se `python` apontar para outra versão, utilize explicitamente o executável do Python 3.12. Exemplo:

```bat
"C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Python312\python.exe" -m venv .venv && .venv\Scripts\activate && python --version
```

O caminho varia conforme a instalação da máquina. Use `where python` para localizar as versões disponíveis.

## 4. Instalar as dependências do projeto

Com a `.venv` ativa:

```bat
python -m pip install --upgrade pip && python -m pip install -r requirements.txt
```

O `requirements.txt` é a fonte oficial das dependências do projeto. As principais são:

```text
robotframework==7.4.2
robotframework-browser==20.2.0
PyYAML==6.0.3
robotframework-requests
robotframework-pabot==5.2.2
```

Não altere versões localmente sem refletir a mudança no `requirements.txt` e validar o pipeline de CI/CD.

## 5. Inicializar Browser Library / Playwright

Depois da instalação Python:

```bat
rfbrowser init
```

Esse comando instala as dependências Node usadas pela Browser Library e baixa os browsers suportados pelo Playwright. Em uma máquina nova ele pode levar alguns minutos.

## 6. Validar toda a instalação

Com a `.venv` ativa, execute:

```bat
python --version && where python && where pip && node --version && npm --version && git --version && robot --version && rfbrowser --version && python -c "import sys; print('Executavel Python:', sys.executable); print('Versao completa:', sys.version)"
```

A validação esperada é:

```text
Python                -> 3.12.x
Python ativo          -> <projeto>\.venv\Scripts\python.exe
Node.js               -> instalado
npm                   -> instalado
Git                   -> instalado
Robot Framework       -> 7.4.2 / Python 3.12.x
Browser Library       -> 20.2.0
Playwright requerido  -> 1.62.0
```

Também é possível validar os imports principais:

```bat
python -c "import robot, Browser, requests, yaml; print('Dependencias Python: OK')" && rfbrowser --version
```

## 7. Script de preparação para Windows

O projeto também possui:

```text
scripts\preparar_ambiente_windows.bat
```

Ele é um atalho para instalar dependências e inicializar o Browser Library. Para a primeira configuração de uma máquina, recomenda-se seguir o passo a passo desta seção para validar cada pré-requisito e confirmar que a `.venv` utiliza Python 3.12.

## Problemas comuns na instalação

### A `.venv` foi criada com a versão errada do Python

Sintoma:

```text
robot --version
Robot Framework ... (Python 3.14.x ...)
```

Mesmo que Python 3.12 esteja instalado, outra versão pode estar primeiro no `PATH`. Verifique:

```bat
python --version && where python && where pip
```

Se necessário, recrie a `.venv` com o caminho explícito do Python 3.12.

### `node` ou `npm` não é reconhecido

Instale o Node.js e abra um novo terminal para que o `PATH` seja recarregado. Depois valide:

```bat
node --version && npm --version
```

### `rfbrowser` não é reconhecido

Confirme que a `.venv` está ativa e que `robotframework-browser` foi instalado:

```bat
where python && where pip && pip show robotframework-browser && rfbrowser --version
```

### Browser Library instalada, mas browsers ainda não disponíveis

Execute novamente:

```bat
rfbrowser init
```

---

# Configuração do ambiente HOT

As configurações não sensíveis ficam em:

```text
data/ambientes/hml.yaml
```

Informações sensíveis, como usuário, senha, token ou segredo, **não devem ser commitadas no repositório**. Elas devem ser fornecidas por variáveis de ambiente ou pelo mecanismo de secrets utilizado pelo projeto.

Antes da primeira execução real, confirme:

- URL do HOT;
- ambiente correto;
- credenciais disponíveis;
- permissões do usuário de automação;
- Nota Fiscal/massa adequada para o cenário;
- arquivos de laudo necessários em `data/fixtures/laudos/`.

---

# Como executar os testes

Todas as execuções locais devem preferencialmente gerar resultados dentro de `reports/`.

## Executar todos os testes

```bat
robot --outputdir reports tests
```

Ou utilize:

```bat
scripts\executar_testes.bat
```

## Executar um arquivo de testes específico

Exemplo:

```bat
robot --outputdir reports tests\hot\inventario\defeito\inventario_defeito.robot
```

> O arquivo acima será criado quando os primeiros cenários reais forem implementados.

## Executar apenas um caso de teste

```bat
robot --outputdir reports --test "Criar Inventário Com Defeito Dentro Da Garantia E Com Peça" tests\hot\inventario\defeito\inventario_defeito.robot
```

Também é possível utilizar `-t`:

```bat
robot --outputdir reports -t "Criar Inventário Com Defeito Dentro Da Garantia E Com Peça" tests\hot\inventario\defeito\inventario_defeito.robot
```

## Executar por tag

Quando os cenários possuírem tags, por exemplo `defeito`, `smoke` ou `regressao`:

```bat
robot --outputdir reports --include defeito tests
```

ou:

```bat
robot --outputdir reports -i smoke tests
```

## Execução paralela

Quando o conjunto de testes estiver preparado para paralelismo:

```bat
pabot --processes 4 --outputdir reports tests
```

O paralelismo só deve ser habilitado para cenários cuja massa e estado da aplicação permitam execução independente.

---

# Relatórios e evidências

O Robot Framework gera, por padrão:

```text
reports/
├── output.xml
├── log.html
└── report.html
```

Além desses artefatos, o framework possui capacidades para evidências e observabilidade que serão conectadas aos cenários reais do HOT conforme a implementação avançar.

Os relatórios locais não devem ser versionados no Git.

---

# Massa de dados e cleanup

A estratégia do projeto prevê que os testes possam:

1. gerar dados únicos quando necessário;
2. registrar a massa criada durante a execução;
3. utilizar essa massa no cenário;
4. validar o resultado;
5. limpar ou restaurar os dados ao final quando o HOT permitir.

Para o fluxo de Inventário, **Número do Ativo** e **Serial** são candidatos naturais a geração dinâmica.

O cleanup não deve ser implementado como uma ação genérica sem conhecer as regras do HOT. Primeiro será validado qual operação real permite excluir, cancelar ou restaurar o ativo em cada estado.

---

# CI/CD

O projeto utiliza **GitHub Actions**.

Workflow:

```text
.github/workflows/ci.yml
```

O pipeline é disparado em:

- `push` para `main` e `develop`;
- Pull Requests para `main` e `develop`;
- execução manual por `workflow_dispatch`.

## Fluxo atual do pipeline

```text
Checkout do repositório
        ↓
Configuração do Python 3.12
        ↓
Instalação das dependências
        ↓
Validação da instalação do Robot Framework
        ↓
Execução dos testes quando existirem suítes .robot
        ↓
Publicação dos relatórios como artefatos
```

Nesta fase inicial, o objetivo do CI é garantir que o projeto possa ser preparado de forma reproduzível. Conforme os testes reais do HOT forem adicionados, o mesmo pipeline passa a executar as suítes automatizadas.

A regra do projeto é: **nenhuma alteração relevante deve ser integrada à branch principal com pipeline quebrado**.

---

# Estratégia de locators

Nenhum locator específico do HOT deve ser criado por adivinhação a partir de screenshots.

Cada elemento deve ser inspecionado no DOM real e registrado no Page Object somente após validação.

Ordem de preferência, quando disponível:

1. identificadores estáveis criados para automação, como `data-testid`;
2. `id` ou `name` estáveis;
3. role + nome acessível;
4. texto estável e específico;
5. relações estruturais estáveis;
6. CSS/XPath somente quando necessário.

Evitar seletores baseados em posição, classes geradas dinamicamente ou XPath absoluto.

Mais detalhes: `docs/estrategia/locators.md`.

---

# Primeiro domínio automatizado — Inventário com Defeito

O fluxo-base começa com a criação do inventário **sem associação de funcionário**. Essa é uma regra funcional importante porque associar o funcionário altera as ações disponíveis e impede o caminho de declaração de defeito usado nesses cenários.

Os seis cenários já mapeados estão documentados em:

```text
docs/casos-de-teste/fluxos-defeito-inventario.md
```

Resumo:

| ID | Cenário | Resultado esperado |
|---|---|---|
| DEF-001 | Dentro da garantia + sem peça | `AGUARDANDO PEÇA` |
| DEF-002 | Dentro da garantia + com peça | `AGUARDANDO REPARO` |
| DEF-003 | Fora da garantia + reparo aprovado | `AGUARDANDO REPARO` |
| DEF-004 | Fora da garantia + reparo reprovado + máquina funcional | `EM ESTOQUE — Equipamento com Defeito mas Funcional` |
| DEF-005 | Fora da garantia + reparo reprovado + máquina não funcional | `REPARO NÃO AUTORIZADO — Equipamento com defeito e não funcional` |
| DEF-006 | Fornecedor Outros | `AGUARDANDO LAUDO` / fluxo atualmente bloqueado para investigação |

Nos cenários DEF-004 e DEF-005, o HOT apresenta o status em duas linhas, porém a combinação representa **um único status de negócio** e deve ser validada como tal.

---

# Fluxo de desenvolvimento

Para cada nova automação do HOT:

```text
Entender a regra de negócio
        ↓
Documentar o cenário
        ↓
Inspecionar o DOM real
        ↓
Definir locators estáveis
        ↓
Implementar Page Object
        ↓
Implementar Keyword de Negócio
        ↓
Implementar Test Case
        ↓
Executar localmente
        ↓
Validar evidências e cleanup
        ↓
Pull Request
        ↓
CI/CD verde
        ↓
Merge
```

---

# Próximo passo técnico

A próxima atividade é iniciar a navegação real do HOT e capturar os elementos do DOM, começando por:

1. Controle de Equipamentos;
2. Cadastro de Estoque;
3. seleção da Nota Fiscal;
4. Localização do Equipamento;
5. Configurações do Equipamento;
6. Número do Ativo e Serial;
7. Adicionar e Salvar;
8. Mais Opções / Ações / Defeito;
9. Dados HITSS;
10. Dados do Fornecedor;
11. Garantia e disponibilidade de peça;
12. validação do status final.

O primeiro cenário que será implementado ponta a ponta é o **DEF-002 — Dentro da garantia + com peça → AGUARDANDO REPARO**, pois é o fluxo que já possui evidências funcionais completas.

---

# Documentação complementar

- Arquitetura: `docs/arquitetura/visao-geral.md`
- Fluxos de Defeito: `docs/casos-de-teste/fluxos-defeito-inventario.md`
- Estratégia de locators: `docs/estrategia/locators.md`
- Histórico de versões: `CHANGELOG.md`

Este README deve permanecer como o **ponto inicial de consulta do projeto**. Sempre que instalação, arquitetura, execução, CI/CD ou convenções importantes forem alteradas, este documento deve ser atualizado junto com o código.
