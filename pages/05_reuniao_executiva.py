import streamlit as st

from src.data.mock_data import alerts, scenarios
from src.ui import metric_card, page_header


page_header(
    "Reunião executiva",
    "Uma decisão, uma versão e responsáveis claros",
    "A diretoria escolhe o cenário e transforma a recomendação em plano oficial.",
)

recommended = st.session_state.get("recommended_scenario", "Base")
data = scenarios().set_index("Cenário")
row = data.loc[recommended]

st.markdown(f"### Cenário recomendado: **{recommended}**")
cards = st.columns(4)
with cards[0]:
    metric_card("Receita atendida", f'R$ {row["Receita atendida (R$ MM)"]:.1f} MM'.replace(".", ","))
with cards[1]:
    metric_card("Receita em risco", f'R$ {row["Receita em risco (R$ MM)"]:.1f} MM'.replace(".", ","))
with cards[2]:
    metric_card("Margem operacional", f'{row["Margem operacional (%)"]:.1f}%'.replace(".", ","))
with cards[3]:
    metric_card("Filiais com gap", str(int(row["Filiais com gap"])))

left, right = st.columns([1.3, 1], gap="large")
with left:
    st.subheader("Riscos materiais")
    st.dataframe(alerts(), hide_index=True, use_container_width=True)
with right:
    st.subheader("Registro da decisão")
    decision = st.text_area("Direcionamento executivo", value="Aprovar cenário Base condicionado à validação do transbordo em CWB.")
    owner = st.text_input("Responsável pela consolidação", value="Inteligência de Mercado")
    deadline = st.date_input("Prazo")
    c1, c2 = st.columns(2)
    if c1.button("Aprovar cenário", type="primary", use_container_width=True):
        st.session_state["executive_status"] = "Aprovado"
        st.success("Cenário aprovado na sessão demonstrativa.")
    if c2.button("Solicitar revisão", use_container_width=True):
        st.session_state["executive_status"] = "Revisão solicitada"
        st.warning("Cenário devolvido para revisão.")

status = st.session_state.get("executive_status", "Pendente")
st.info(f"Status da decisão: {status} | Versão proposta: SOP_2026_08_v01")

