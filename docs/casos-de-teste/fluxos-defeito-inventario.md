# HOT — Cadastro de Estoque — Fluxos de Defeito

## Regra comum

O inventário deve ser criado **sem preencher dados de funcionário** antes de declarar o defeito. O vínculo com funcionário altera as ações disponíveis para o equipamento.

## Fluxo-base

1. Acessar Controle de Equipamentos.
2. Iniciar Cadastro de Estoque.
3. Selecionar Nota Fiscal válida.
4. Informar Localização do Equipamento.
5. Informar Configurações do Equipamento.
6. Informar Número do Ativo e Serial.
7. Adicionar o ativo.
8. Salvar.
9. Validar criação.
10. Não associar funcionário.
11. Acessar Mais Opções → Ações.
12. Alterar status para DEFEITO.
13. Informar Chamado HITSS.
14. Anexar Laudo HITSS.
15. Selecionar Tipo(s) de Defeito.
16. Informar comentário.
17. Salvar e validar DEFEITO.
18. Prosseguir para Dados de Manutenção.

## DEF-001 — Dentro da garantia e sem peça

- Garantia: Sim
- Tem peça: Não
- Resultado: **AGUARDANDO PEÇA**

## DEF-002 — Dentro da garantia e com peça

- Garantia: Sim
- Tem peça: Sim
- Resultado: **AGUARDANDO REPARO**
- Este será o primeiro cenário automatizado.

## DEF-003 — Fora da garantia e reparo aprovado

- Garantia: Não
- Reparo aprovado: Sim
- Resultado: **AGUARDANDO REPARO**
- Os estados intermediários do fluxo também devem ser validados.

## DEF-004 — Fora da garantia, reparo reprovado e máquina funcional

- Garantia: Não
- Reparo aprovado: Não
- Estado da máquina: Máquina funcional
- Status completo esperado:

```text
EM ESTOQUE
Equipamento com Defeito mas Funcional
```

As duas linhas representam um **único status de negócio**.

## DEF-005 — Fora da garantia, reparo reprovado e máquina não funcional

- Garantia: Não
- Reparo aprovado: Não
- Estado da máquina: Máquina não funcional
- Status completo esperado:

```text
REPARO NÃO AUTORIZADO
Equipamento com defeito e não funcional
```

As duas linhas representam um **único status de negócio**.

## DEF-006 — Fornecedor Outros

- Fornecedor: Outro/Outros
- Estado observado: **AGUARDANDO LAUDO**
- Comportamento observado: o campo necessário para anexar o laudo não é disponibilizado e o fluxo fica bloqueado.
- Classificação atual: **possível defeito / known issue**, pendente de confirmação formal do requisito.

## Validações comuns

Quando aplicável, cada cenário deve validar:

- status completo do ativo;
- dados de manutenção persistidos;
- documentos anexados;
- histórico de atividades;
- ativo e serial corretos;
- resultado na listagem do Controle de Equipamentos.

## Massa de dados

Número do Ativo e Serial devem ser gerados dinamicamente. Toda massa criada pela automação deve ser registrada para cleanup quando o HOT permitir a remoção ou restauração segura do dado.
