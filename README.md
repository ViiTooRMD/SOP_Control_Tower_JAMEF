# S&OP Control Tower JAMEF

Draft funcional de uma aplicação Streamlit para operar o ciclo de S&OP da JAMEF, conectando previsão de demanda, capacidade operacional, cenários, impacto financeiro, decisão executiva e S&OE.

## Visão do produto

```text
Revisão da Demanda
        ↓
Revisão de Capacidade
        ↓
Construção de Cenários
        ↓
Revisão Financeira
        ↓
Reunião Executiva
        ↓
Plano Oficial e S&OE
```

O draft utiliza dados simulados para validar a experiência, o processo e os componentes visuais antes da integração com BigQuery e com o motor Python de forecast.

## Telas disponíveis

- Torre de Controle;
- Revisão da Demanda;
- Revisão de Capacidade;
- Construção de Cenários;
- Revisão Financeira;
- Reunião Executiva;
- S&OE e gestão de exceções;
- Premissas e governança.

## Executar localmente

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura

```text
app.py
pages/                  # bancadas do ciclo
src/data/               # mocks e futuros adaptadores BigQuery
config/regras.yaml      # regras iniciais do piloto
docs/architecture.md    # arquitetura e integrações futuras
tests/                  # verificações da camada de dados
```

## Regras iniciais representadas

- `TIPO_TRAN = 'ROD'`;
- `TIPO_DOC = 'CTRC'`;
- B2B e B2C;
- Perene: faturamento em pelo menos 12 meses ou 3 meses acima de R$ 200 mil;
- Spot: demais clientes, tratado por rota;
- Perene tratado por cliente e rota;
- Origem consome coleta, passagens consomem transbordo e destino consome entrega;
- Cenários Conservador, Base e Agressivo;
- Plano aprovado versionado como one set of numbers.

## Status

Versão `draft-01`: interface completa com dados simulados. Próxima etapa: conectar a Revisão da Demanda ao output real do motor e homologar capacidade, produtividade e shares de transbordo.

