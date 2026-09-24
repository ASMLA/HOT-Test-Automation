# Histórico de Alterações

Todas as mudanças relevantes deste projeto serão registradas aqui.

## [Unreleased]

### Implementação

- Implementado o primeiro cenário real `HOT-INV-DEF-001 - Defeito Dentro Da Garantia Sem Peça`.
- Adicionados locators reais validados pelo mapeamento Playwright.
- Adicionadas keywords de negócio para criação do inventário, defeito, garantia, peça e retorno ao estoque.
- Adicionada massa dinâmica para Armário, Ativo, Serial e chamados.
- Adicionadas fixtures PDF seguras para os laudos de teste.
- Saídas de mapeamento JSON/TXT passam a ser ignoradas pelo Git.

### Ponto para validar no primeiro run

- A regra manual de "3ª opção da combo" está implementada como índice zero-based `2`.
- O cenário parte da Home do HOT e pressupõe autenticação disponível para a sessão.

## [0.1.0] - 2026-09-01

### Documentação

- README expandido com arquitetura, execução local, CI/CD, relatórios, massa de dados e fluxo de desenvolvimento.
- Adicionado guia detalhado de preparação de uma máquina do zero, incluindo Python 3.12, Node.js/npm, Git, `.venv`, instalação das dependências, `rfbrowser init`, validação completa e troubleshooting.
- CI atualizado para validar Python 3.12, instalar dependências, inicializar Browser Library/Playwright, validar a stack e executar suítes Robot quando existirem.
- `.gitignore` reforçado para impedir versionamento de `.venv`, relatórios, segredos, arquivos de IDE e evidências locais.
- Script Windows de preparação atualizado para validar pré-requisitos, criar/ativar `.venv`, instalar dependências e inicializar o Browser Library.

### Adicionado

- Criação do projeto independente de automação do HOT.
- Utilização do Automation Diary Framework v0.24.0 como baseline técnico.
- Remoção do histórico e da documentação do Automation Diary do novo projeto.
- Estrutura inicial para Page Objects e Keywords de negócio do HOT.
- Especificação consolidada dos seis fluxos de Defeito do Cadastro de Estoque.
- Estratégia para captura e governança de locators reais.
- Estrutura para massa de dados, laudos, configuração e execução em CI/CD.

### Próximo passo

- Mapear os locators reais no DOM do HOT e implementar a navegação do primeiro cenário: dentro da garantia + com peça → `AGUARDANDO REPARO`.
