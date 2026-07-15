import streamlit as st

from src.data.mock_data import scenarios
from src.ui import metric_card, page_header


page_header(
    "Revisão financeira",
    "O custo da resposta precisa proteger receita e margem",
    "Comparação econômica dos cenários operacionais antes da decisão executiva.",
)

data = scenarios().set_index("Cenário")
base = data.loc["Base"]

cards = st.columns(4)
with cards[0]:
    metric_card("Receita atendida", f'R$ {base["Receita atendida (R$ MM)"]:.1f} MM'.replace(".", ","))
with cards[1]:
    metric_card("Receita em risco", f'R$ {base["Receita em risco (R$ MM)"]:.1f} MM'.replace(".", ","))
with cards[2]:
    metric_card("Custo incremental", f'R$ {base["Custo incremental (R$ MM)"]:.1f} MM'.replace(".", ","))
with cards[3]:
    metric_card("Margem operacional", f'{base["Margem operacional (%)"]:.1f}%'.replace(".", ","))

left, right = st.columns(2, gap="large")
with left:
    st.subheader("Receita atendida e em risco")
    st.bar_chart(data[["Receita atendida (R$ MM)", "Receita em risco (R$ MM)"]], color=["#17212B", "#C8102E"], height=330)
with right:
    st.subheader("Custo incremental por cenário")
    st.bar_chart(data[["Custo incremental (R$ MM)"]], color="#C8102E", height=330)

st.subheader("Quadro de decisão financeira")
st.dataframe(data, use_container_width=True)
st.success("Recomendação preliminar: cenário Base equilibra cobertura operacional, receita protegida e margem.")

