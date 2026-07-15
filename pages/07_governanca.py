import streamlit as st

from src.data.mock_data import gates
from src.ui import page_header, stage_flow


page_header(
    "Governança",
    "O processo avança por gates, evidências e versões",
    "As regras do piloto ficam explícitas para BigQuery, Python, Streamlit e áreas participantes.",
)

st.subheader("Gates de decisão")
st.dataframe(gates(), hide_index=True, use_container_width=True)

st.subheader("Princípios do piloto")
st.markdown(
    """
    - BigQuery mantém os dados oficiais e as versões aprovadas.
    - Python executa forecast, backtesting, apropriação da malha e cenários.
    - Streamlit organiza inputs, validações, comparações e decisões.
    - GitHub versiona código, regras, documentação e mudanças do modelo.
    - O plano aprovado é imutável; qualquer alteração gera uma nova versão.
    """
)

st.subheader("Regras que exigem homologação")
st.warning(
    "Prioridades atuais: calendário de dias úteis, capacidade nominal, produtividade de referência, "
    "limites de ocupação e validação do transbordo. A regra Perene × Spot adotada neste projeto é: "
    "PERENE quando houver faturamento em pelo menos 12 meses ou em 3 meses acima de R$ 200 mil; demais SPOT."
)

st.subheader("Arquitetura funcional")
st.code("Fontes → BigQuery → Motor Python → Streamlit → Plano oficial → S&OE", language="text")

