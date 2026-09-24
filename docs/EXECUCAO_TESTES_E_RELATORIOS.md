# Execução dos Testes e Relatórios — HOT Test Automation

Execute os comandos a partir da raiz do projeto `HOT-Test-Automation`.

## 1. Executar um teste específico

Exemplo — DEF-001:

```bat
.venv\Scripts\python.exe -m robot --outputdir reports --loglevel INFO tests\hot\inventario\defeito\HOT-INV-DEF-001.robot
```

Para outro cenário, altere somente o arquivo final para `HOT-INV-DEF-002.robot`, `HOT-INV-DEF-003.robot`, `HOT-INV-DEF-004.robot` ou `HOT-INV-DEF-005.robot`.

## 2. Executar todos os testes de defeito

```bat
.venv\Scripts\python.exe -m robot --outputdir reports --loglevel INFO tests\hot\inventario\defeito
```

Artefatos padrão:

```text
reports\output.xml
reports\log.html
reports\report.html
reports\evidencias\<SCENARIO-ID>\
```

## 3. Gerar somente o relatório consolidado

Quando os testes já tiverem sido executados:

```bat
gerar_relatorio_com_checks.bat
```

Saída principal:

```text
reports\relatorio_consolidado.html
```

O consolidado separa casos de teste de checks de negócio e apresenta as evidências diretamente abaixo de cada check. Screenshot isolada não é considerada aprovação: o resultado do check vem da execução registrada no `output.xml`.

## 4. Executar todos os testes + gerar relatório

```bat
rodar_todos_defeitos_com_relatorio.bat
```

Fluxo:

```text
DEF-001 → DEF-002 → DEF-003 → DEF-004 → DEF-005
        → output.xml → checks → evidências → relatório consolidado
```

## 5. Resumo rápido

| Objetivo | Comando |
|---|---|
| Um teste | `.venv\Scripts\python.exe -m robot --outputdir reports --loglevel INFO tests\hot\inventario\defeito\HOT-INV-DEF-001.robot` |
| Todos os testes | `.venv\Scripts\python.exe -m robot --outputdir reports --loglevel INFO tests\hot\inventario\defeito` |
| Só relatório | `gerar_relatorio_com_checks.bat` |
| Tudo + relatório | `rodar_todos_defeitos_com_relatorio.bat` |

## 6. Estado atual

Cenários automatizados: DEF-001 a DEF-005.

Relatório atual: 5 casos de teste e 63 checks planejados.

## 7. Regras

- Não versionar credenciais.
- Login/MFA permanece manual com sessão persistente.
- `reports/evidencias/`, `.browser-profile/` e `.test-runtime/` permanecem ignorados pelo Git.
- Etapas funcionais já validadas permanecem congeladas até existir necessidade comprovada de alteração.
- Melhorias de relatório não alteram o fluxo funcional.
