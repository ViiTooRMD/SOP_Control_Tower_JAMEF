import pandas as pd
import streamlit as st

from src.data.mock_data import commercial_inputs, demand_mix, weekly_demand
from src.ui import metric_card, page_header


page_header(
    "Revisão da demanda",
    "Do baseline estatístico ao número consensado",
    "A ponte entre histórico, efeito B2C e julgamento comercial fica visível e versionada.",
)

f1, f2, f3, f4 = st.columns(4)
with f1:
    st.selectbox("Métrica", ["Frete", "Peso cubado", "Volumes", "CTEs"])
with f2:
    st.multiselect("Operação", ["B2B", "B2C"], default=["B2B", "B2C"])
with f3:
    st.multiselect("Perfil", ["Perene", "Spot"], default=["Perene", "Spot"])
with f4:
    st.selectbox("Visão", ["Semanal", "Mensal"])

demand = weekly_demand()
mix = demand_mix()

cards = st.columns(4)
with cards[0]:
    metric_card("WAPE", "7,8%", "-1,4 p.p. vs. ciclo anterior")
with cards[1]:
    metric_card("BIAS", "+1,9%", "Leve superprevisão")
with cards[2]:
    metric_card("Ajuste comercial", "+3,1%", "Sobre o baseline")
with cards[3]:
    metric_card("Share B2C final", f'{mix["Share B2C"].iloc[-1]:.0%}', "Cenário Base")

left, right = st.columns([1.55, 1], gap="large")
with left:
    st.subheader("Baseline × forecast final")
    st.line_chart(demand.set_index("Semana")[["Baseline", "Forecast final"]], color=["#8B95A1", "#C8102E"], height=320)
with right:
    st.subheader("Evolução do mix")
    st.area_chart(mix.set_index("Semana")[["B2B", "B2C"]], color=["#17212B", "#C8102E"], height=320)

st.subheader("Inputs comerciais registrados")
st.dataframe(commercial_inputs(), hide_index=True, use_container_width=True)

with st.expander("Registrar novo input comercial", expanded=False):
    with st.form("commercial_input"):
        c1, c2, c3 = st.columns(3)
        client = c1.text_input("Cliente ou grupo")
        route = c2.text_input("Rota", placeholder="SAO_CWB")
        input_type = c3.selectbox("Tipo", ["SOW", "Risco de churn", "Entrada de cliente", "Campanha", "Evento"])
        c4, c5 = st.columns(2)
        adjustment = c4.slider("Ajuste (%)", -50, 100, 0)
        confidence = c5.slider("Confiança (%)", 0, 100, 70)
        justification = st.text_area("Justificativa")
        submitted = st.form_submit_button("Registrar input", type="primary")
        if submitted:
            if not client or not route or not justification:
                st.error("Cliente, rota e justificativa são obrigatórios.")
            else:
                st.session_state["last_commercial_input"] = {
                    "Cliente": client,
                    "Rota": route,
                    "Tipo": input_type,
                    "Ajuste": adjustment,
                    "Confiança": confidence,
                    "Justificativa": justification,
                }
                st.success("Input registrado nesta sessão demonstrativa.")

bridge = pd.DataFrame(
    {"Etapa": ["Baseline", "SOW e entradas", "Churn", "Efeito B2C", "Forecast final"], "R$ MM": [472.1, 12.8, -5.4, 7.3, 486.8]}
).set_index("Etapa")
st.subheader("Ponte de construção do forecast")
st.bar_chart(bridge, color="#C8102E", horizontal=True)

