import streamlit as st

from src.ui import inject_css


st.set_page_config(
    page_title="S&OP Control Tower | JAMEF",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

pages = {
    "Ciclo S&OP": [
        st.Page("pages/00_torre_controle.py", title="Torre de Controle", icon="🏠", default=True),
        st.Page("pages/01_revisao_demanda.py", title="Revisão da Demanda", icon="📈"),
        st.Page("pages/02_revisao_capacidade.py", title="Revisão de Capacidade", icon="🏭"),
        st.Page("pages/03_cenarios.py", title="Construção de Cenários", icon="🧭"),
        st.Page("pages/04_revisao_financeira.py", title="Revisão Financeira", icon="💰"),
        st.Page("pages/05_reuniao_executiva.py", title="Reunião Executiva", icon="✅"),
    ],
    "Execução e governança": [
        st.Page("pages/06_soe.py", title="S&OE e Exceções", icon="⚠️"),
        st.Page("pages/07_governanca.py", title="Premissas e Governança", icon="📚"),
    ],
}

with st.sidebar:
    st.markdown("## S&OP Control Tower")
    st.caption("Piloto JAMEF · ambiente demonstrativo")
    st.selectbox("Ciclo", ["Agosto/2026"], key="cycle")
    st.selectbox("Cenário de trabalho", ["Base", "Conservador", "Agressivo"], key="scenario")
    st.caption("Horizonte: semana atual + 7 semanas")

navigation = st.navigation(pages, position="sidebar")
navigation.run()

