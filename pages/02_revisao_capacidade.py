import streamlit as st

from src.data.mock_data import capacity_detail
from src.ui import metric_card, page_header


page_header(
    "Revisão de capacidade",
    "Onde a demanda encontra a restrição operacional",
    "Apropriação por coleta, transbordo, transferência e entrega, com leitura por filial.",
)

data = capacity_detail()
filiais = st.multiselect("Filiais", sorted(data["Filial"].unique()), default=sorted(data["Filial"].unique()))
processo = st.selectbox("Processo", ["Todos"] + sorted(data["Processo"].unique()))
filtered = data[data["Filial"].isin(filiais)].copy()
if processo != "Todos":
    filtered = filtered[filtered["Processo"] == processo]

critical = int((filtered["Status"] == "Crítico").sum())
attention = int((filtered["Status"] == "Atenção").sum())
avg_occupancy = filtered["Ocupação"].mean() if not filtered.empty else 0
total_gap = filtered["Gap"].sum() if not filtered.empty else 0

cards = st.columns(4)
with cards[0]:
    metric_card("Ocupação média", f"{avg_occupancy:.0%}")
with cards[1]:
    metric_card("Pontos críticos", str(critical))
with cards[2]:
    metric_card("Pontos em atenção", str(attention))
with cards[3]:
    metric_card("Gap consolidado", f"{total_gap:,.0f}".replace(",", "."), "Capacidade − demanda")

left, right = st.columns([1.25, 1], gap="large")
with left:
    st.subheader("Ocupação por filial e processo")
    pivot = filtered.pivot(index="Filial", columns="Processo", values="Ocupação")
    st.dataframe(pivot.style.format("{:.0%}").background_gradient(cmap="RdYlGn_r", vmin=0.75, vmax=1.15), use_container_width=True)
with right:
    st.subheader("Demanda versus capacidade")
    comparison = filtered.groupby("Filial")[["Demanda", "Capacidade"]].sum()
    st.bar_chart(comparison, color=["#C8102E", "#17212B"], height=315)

st.subheader("Detalhamento operacional")
display = filtered.copy()
display["Ocupação"] = display["Ocupação"].map(lambda value: f"{value:.1%}")
st.dataframe(display, hide_index=True, use_container_width=True)

st.info("Validação do piloto: coleta e entrega devem reconciliar 100% com o projetado; o transbordo permanece como check específico da malha.")

