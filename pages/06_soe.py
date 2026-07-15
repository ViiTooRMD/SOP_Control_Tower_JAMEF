import streamlit as st

from src.data.mock_data import actions, deviations
from src.ui import metric_card, page_header


page_header(
    "S&OE",
    "Gestão semanal orientada por exceções",
    "O plano aprovado vira referência; apenas desvios materiais entram na pauta operacional.",
)

data = deviations()
cards = st.columns(4)
with cards[0]:
    metric_card("Exceções abertas", str((data["Tratamento"] == "Ação necessária").sum()))
with cards[1]:
    metric_card("Maior desvio", f'{data["Desvio (%)"].abs().max():.1f}%'.replace(".", ","))
with cards[2]:
    metric_card("Ações abertas", str(len(actions())))
with cards[3]:
    metric_card("SLA de tratamento", "48 horas")

st.subheader("Plano versus realizado")
st.dataframe(data, hide_index=True, use_container_width=True)

chart = data.set_index("Filial")[["Desvio (%)"]]
st.bar_chart(chart, color="#C8102E", height=300)

st.subheader("Plano corretivo")
st.dataframe(actions(), hide_index=True, use_container_width=True)

