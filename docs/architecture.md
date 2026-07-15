# Arquitetura funcional

O piloto separa claramente a responsabilidade de cada camada:

```text
Fontes operacionais e comerciais
              ↓
BigQuery — dados oficiais e versões
              ↓
Python — forecast, backtesting, malha e cenários
              ↓
Streamlit — inputs, validações, comparação e decisão
              ↓
Plano S&OP aprovado — one set of numbers
              ↓
S&OE — plano versus realizado e gestão de exceções
```

## Camadas previstas

- `src/data`: dados simulados no draft; futuramente adaptadores BigQuery.
- `src/forecast`: motor estatístico e backtesting.
- `src/capacity`: apropriação da demanda e cálculo de gaps.
- `src/finance`: custos, margem, LAJIR e ponto de equilíbrio.
- `src/governance`: versões, gates, decisões e auditoria.
- `pages`: bancadas de trabalho do ciclo S&OP.

## Dados oficiais

A base histórica principal será `jamef-dados-prd.gold_dw_jamef.fato_cif_fob_bi`, com filtros:

- `TIPO_TRAN = 'ROD'`;
- `TIPO_DOC = 'CTRC'`;
- `OPER_B2B_B2C IN ('B2B', 'B2C')`;
- `CAP_INT_DESTINO IN ('CAPITAL', 'INTERIOR 1', 'INTERIOR 2')`.

## Próximas integrações

1. Substituir `src/data/mock_data.py` por consultas versionadas ao BigQuery.
2. Importar o output do motor de forecast para a Revisão da Demanda.
3. Carregar `Share_Historico` na Revisão de Capacidade.
4. Persistir inputs comerciais, gates e decisões.
5. Implementar autenticação e alçadas.

