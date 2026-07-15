from __future__ import annotations

import html
from typing import Iterable

import streamlit as st


JAMEF_RED = "#C8102E"
INK = "#17212B"


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root { --jamef-red:#C8102E; --ink:#17212B; --muted:#65707D; --line:#E1E5EA; }
        .stApp { background: #F6F7F9; }
        [data-testid="stSidebar"] { background: #17212B; }
        [data-testid="stSidebar"] * { color: #F7F8FA; }
        [data-testid="stSidebar"] input { color: #17212B !important; }
        .block-container { padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1480px; }
        .sop-eyebrow { color: var(--jamef-red); font-weight: 800; letter-spacing: .08em; font-size: .78rem; }
        .sop-title { color: var(--ink); font-size: 2.1rem; line-height: 1.1; font-weight: 800; margin:.2rem 0 .35rem; }
        .sop-subtitle { color: var(--muted); margin-bottom: 1.1rem; }
        .metric-card { background:#FFF; border:1px solid var(--line); border-radius:14px; padding:16px 18px; min-height:118px; box-shadow:0 4px 12px rgba(23,33,43,.04); }
        .metric-label { color:var(--muted); font-size:.82rem; font-weight:700; text-transform:uppercase; letter-spacing:.03em; }
        .metric-value { color:var(--ink); font-size:1.7rem; font-weight:800; margin-top:.35rem; }
        .metric-delta { color:#26845B; font-size:.82rem; margin-top:.15rem; }
        .stage-card { background:#FFF; border:1px solid var(--line); border-top:5px solid #D6DBE1; border-radius:12px; padding:13px; min-height:132px; }
        .stage-card.active { border-top-color:var(--jamef-red); background:#FFF8F9; }
        .stage-card.done { border-top-color:#26845B; }
        .stage-name { color:var(--ink); font-weight:800; font-size:.95rem; }
        .stage-status { color:var(--muted); font-size:.78rem; margin:.35rem 0; }
        .stage-owner { color:var(--jamef-red); font-size:.75rem; font-weight:700; }
        .panel-title { color:var(--ink); font-size:1.05rem; font-weight:800; margin:.4rem 0 .8rem; }
        .decision-box { background:#17212B; color:#FFF; padding:18px 20px; border-radius:14px; }
        .decision-box strong { color:#FFF; }
        div[data-testid="stMetric"] { background:#FFF; border:1px solid var(--line); padding:14px; border-radius:12px; }
        div[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:10px; overflow:hidden; }
        .stButton>button[kind="primary"] { background:var(--jamef-red); border-color:var(--jamef-red); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(kicker: str, title: str, subtitle: str) -> None:
    st.markdown(f'<div class="sop-eyebrow">{html.escape(kicker.upper())}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sop-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sop-subtitle">{html.escape(subtitle)}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, delta: str = "") -> None:
    delta_html = f'<div class="metric-delta">{html.escape(delta)}</div>' if delta else ""
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{html.escape(label)}</div>'
        f'<div class="metric-value">{html.escape(value)}</div>{delta_html}</div>',
        unsafe_allow_html=True,
    )


def stage_flow(stages: Iterable[dict]) -> None:
    items = list(stages)
    columns = st.columns(len(items), gap="small")
    for column, stage in zip(columns, items):
        with column:
            css_class = stage.get("class", "")
            st.markdown(
                f'<div class="stage-card {css_class}">'
                f'<div class="stage-name">{html.escape(stage["name"])}</div>'
                f'<div class="stage-status">{html.escape(stage["status"])}</div>'
                f'<div class="stage-owner">{html.escape(stage["owner"])}</div>'
                "</div>",
                unsafe_allow_html=True,
            )


def currency_br(value: float, decimals: int = 1) -> str:
    scaled = value / 1_000_000
    return f"R$ {scaled:,.{decimals}f} MM".replace(",", "X").replace(".", ",").replace("X", ".")

