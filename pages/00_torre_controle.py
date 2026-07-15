import streamlit as st

from src.data.mock_data import actions, alerts, capacity_detail, demand_mix, weekly_demand
from src.ui import currency_br, metric_card, page_header, stage_flow


page_header(
    "Visão executiva",
    "Torre de Controle do S&OP",
    "O ciclo mostra onde estamos, quais decisões estão abertas e onde demanda e capacidade deixam de convergir.",
)

stages = [
    {"name": "Demanda", "status": "Concluída", "owner": "Barbara Opsfelder", "class": "done"},
    {"name": "Capacidade", "status": "Em andamento", "owner": "Ricardo Gonçalves", "class": "active"},
    {"name": "Cenários", "status": "Pendente", "owner": "Operações + áreas", "class": ""},
    {"name": "Financeiro", "status": "Pendente", "owner": "Valerio Dallolio", "class": ""},
    {"name": "Executiva", "status": "Não iniciada", "owner": "Marcos Rodrigues", "class": ""},
    {"name": "S&OE", "status": "Não iniciada", "owner": "IM + áreas", "class": ""},
]
stage_flow(stages)

st.write("")
demand = weekly_demand()
mix = demand_mix()
capacity = capacity_detail()
critical = int((capacity["Status"] == "Crítico").sum())

cards = st.columns(6, gap="small")
with cards[0]:
    metric_card("Receita projetada", currency_br(demand["Forecast final"].sum() * 1_000_000), "+4,8% vs. baseline")
with cards[1]:
    metric_card("Peso cubado", "42,8 mil t", "+6,2% no horizonte")
with cards[2]:
    metric_card("Volumes", "1,84 MM", "+3,7% vs. plano anterior")
with cards[3]:
    metric_card("Share B2C", f'{mix["Share B2C"].iloc[-1]:.0%}', "+13 p.p. no horizonte")
with cards[4]:
    metric_card("Pontos críticos", str(critical), "Filial × processo")
with cards[5]:
    metric_card("Custo incremental", "R$ 0,7 MM", "Cenário Base")

left, right = st.columns([1.65, 1], gap="large")
with left:
    st.markdown('<div class="panel-title">Demanda versus capacidade · R$ MM por semana</div>', unsafe_allow_html=True)
    chart = demand.set_index("Semana")[["Baseline", "Forecast final", "Capacidade"]]
    st.line_chart(chart, color=["#8B95A1", "#C8102E", "#17212B"], height=330)

with right:
    st.markdown('<div class="panel-title">Alertas que exigem decisão</div>', unsafe_allow_html=True)
    st.dataframe(alerts(), hide_index=True, use_container_width=True, height=330)

st.markdown('<div class="panel-title">Ações abertas do ciclo</div>', unsafe_allow_html=True)
st.dataframe(actions(), hide_index=True, use_container_width=True)

st.markdown(
    '<div class="decision-box"><strong>Próximo gate:</strong> G2 — Demanda consensada. '
    'A capacidade só será recalculada após o encerramento dos inputs comerciais e a publicação da versão final do forecast.</div>',
    unsafe_allow_html=True,
)

