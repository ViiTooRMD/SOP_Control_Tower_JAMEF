import pandas as pd
import streamlit as st

from src.data.mock_data import scenarios
from src.ui import metric_card, page_header


page_header(
    "Construção de cenários",
    "Transformar gaps em alternativas comparáveis",
    "Cada ação operacional precisa mostrar capacidade adicionada, custo, risco e impacto no nível de serviço.",
)

selected = st.radio("Cenário de trabalho", ["Conservador", "Base", "Agressivo"], horizontal=True, index=1)

with st.expander("Premissas editáveis do cenário", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    b2c = c1.slider("Crescimento B2C (%)", 0, 30, 12 if selected == "Base" else 5 if selected == "Conservador" else 20)
    overtime = c2.slider("Horas extras", 0, 1500, 700, step=50)
    vehicles = c3.slider("Veículos adicionais", 0, 12, 4)
    hires = c4.slider("Contratações", 0, 20, 5)

capacity_added = overtime * 4.2 + vehicles * 680 + hires * 240
incremental_cost = overtime * 72 + vehicles * 48_000 + hires * 8_500
risk_reduction = min(95, 20 + b2c * 1.2 + vehicles * 5 + hires * 1.5)

cards = st.columns(4)
with cards[0]:
    metric_card("Capacidade adicionada", f"{capacity_added:,.0f}".replace(",", "."))
with cards[1]:
    metric_card("Custo incremental", f"R$ {incremental_cost/1_000_000:.2f} MM".replace(".", ","))
with cards[2]:
    metric_card("Redução do risco", f"{risk_reduction:.0f}%")
with cards[3]:
    metric_card("Gap remanescente", f"{max(0, 8 - vehicles - hires/4):.1f}", "Pontos filial × processo")

st.subheader("Comparativo padrão")
scenario_data = scenarios().set_index("Cenário")
st.dataframe(scenario_data, use_container_width=True)

financial = scenario_data[["Receita atendida (R$ MM)", "Receita em risco (R$ MM)", "Custo incremental (R$ MM)"]]
st.bar_chart(financial, color=["#17212B", "#C8102E", "#8B95A1"], height=330)

if st.button("Selecionar como cenário recomendado", type="primary"):
    st.session_state["recommended_scenario"] = selected
    st.success(f"Cenário {selected} marcado como recomendado nesta sessão.")

