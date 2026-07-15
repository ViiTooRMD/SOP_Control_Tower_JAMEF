from __future__ import annotations

import numpy as np
import pandas as pd


SEED = 20260715


def weekly_demand() -> pd.DataFrame:
    weeks = pd.date_range("2026-07-20", periods=8, freq="W-MON")
    baseline = np.array([55.2, 56.1, 56.8, 58.0, 59.3, 60.6, 62.1, 64.0])
    adjustment = np.array([0.2, 0.4, 0.7, 1.0, 1.4, 2.0, 2.8, 3.6])
    capacity = np.array([58.5, 58.5, 59.0, 59.5, 60.0, 60.5, 61.2, 62.0])
    return pd.DataFrame(
        {
            "Semana": weeks,
            "Baseline": baseline,
            "Forecast final": baseline + adjustment,
            "Capacidade": capacity,
        }
    )


def demand_mix() -> pd.DataFrame:
    weeks = pd.date_range("2026-07-20", periods=8, freq="W-MON")
    total = weekly_demand()["Forecast final"].to_numpy()
    b2c_share = np.array([0.22, 0.23, 0.24, 0.25, 0.27, 0.29, 0.32, 0.35])
    return pd.DataFrame(
        {"Semana": weeks, "B2B": total * (1 - b2c_share), "B2C": total * b2c_share, "Share B2C": b2c_share}
    )


def capacity_detail() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    filiais = ["SAO", "CWB", "BHZ", "RIO", "FOR"]
    processos = ["Coleta", "Transbordo", "Transferência", "Entrega"]
    rows = []
    for filial in filiais:
        base = {"SAO": 14800, "CWB": 9000, "BHZ": 7600, "RIO": 8200, "FOR": 6100}[filial]
        for index, processo in enumerate(processos):
            demanda = round(base * (0.82 + index * 0.05) * rng.uniform(0.93, 1.08))
            capacidade = round(base * rng.uniform(0.88, 1.08))
            ocupacao = demanda / capacidade
            gap = capacidade - demanda
            status = "Crítico" if ocupacao > 1.05 else "Atenção" if ocupacao > 0.92 else "Adequado"
            rows.append([filial, processo, demanda, capacidade, ocupacao, gap, status])
    return pd.DataFrame(rows, columns=["Filial", "Processo", "Demanda", "Capacidade", "Ocupação", "Gap", "Status"])


def scenarios() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Conservador", 5, 400, 2, 1, 0, 58.0, 4.0, 0.30, 12.1, 6],
            ["Base", 12, 700, 4, 3, 5, 61.0, 1.5, 0.70, 13.4, 2],
            ["Agressivo", 20, 1000, 7, 5, 10, 64.0, 0.4, 1.40, 12.8, 1],
        ],
        columns=[
            "Cenário", "Crescimento B2C (%)", "Horas extras", "Veículos", "Agregados", "Contratações",
            "Receita atendida (R$ MM)", "Receita em risco (R$ MM)", "Custo incremental (R$ MM)",
            "Margem operacional (%)", "Filiais com gap",
        ],
    )


def alerts() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Crítico", "CWB", "Transbordo", "Ocupação projetada acima de 108%", "Ricardo Gonçalves"],
            ["Crítico", "SAO", "Entrega", "Gap de capacidade na semana 35", "Operações"],
            ["Atenção", "RIO", "Coleta", "Produtividade 6% abaixo da referência", "Operações"],
            ["Atenção", "—", "Demanda", "Share B2C supera 32% no fim do horizonte", "Barbara Opsfelder"],
        ],
        columns=["Criticidade", "Filial", "Processo", "Alerta", "Owner"],
    )


def actions() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Validar capacidade de transbordo CWB", "Ricardo Gonçalves", "20/07/2026", "Em andamento"],
            ["Confirmar SOW dos 10 maiores clientes", "Comercial", "21/07/2026", "Pendente"],
            ["Homologar custo de horas extras", "Valerio Dallolio", "22/07/2026", "Pendente"],
            ["Validar shares de transbordo", "IM + Operações", "22/07/2026", "Em andamento"],
        ],
        columns=["Ação", "Responsável", "Prazo", "Status"],
    )


def commercial_inputs() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Grupo Alfa", "SAO_CWB", "SOW", 12, 80, "Em análise"],
            ["Cliente Beta", "SAO_RIO", "Risco de churn", -8, 70, "Aprovado"],
            ["Grupo Gama", "BHZ_SAO", "Entrada de cliente", 15, 90, "Pendente"],
        ],
        columns=["Cliente/Grupo", "Rota", "Tipo", "Ajuste (%)", "Confiança (%)", "Status"],
    )


def deviations() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["2026-S29", "SAO", "Frete", 14.2, 14.8, 4.2, "Monitorar"],
            ["2026-S29", "CWB", "Cubagem", 8.4, 9.3, 10.7, "Ação necessária"],
            ["2026-S29", "RIO", "Volumes", 105000, 101000, -3.8, "Dentro da tolerância"],
            ["2026-S29", "BHZ", "CTEs", 15400, 16900, 9.7, "Ação necessária"],
        ],
        columns=["Semana", "Filial", "Métrica", "Plano", "Realizado", "Desvio (%)", "Tratamento"],
    )


def gates() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["G0", "Escopo aprovado", "Concluído", "Sponsor do piloto"],
            ["G1", "Dados reconciliados", "Em andamento", "Inteligência de Mercado"],
            ["G2", "Demanda consensada", "Pendente", "Barbara Opsfelder"],
            ["G3", "Capacidade validada", "Pendente", "Ricardo Gonçalves"],
            ["G4", "Cenário aprovado", "Pendente", "Marcos Rodrigues"],
            ["G5", "Piloto avaliado", "Pendente", "Sponsor do piloto"],
        ],
        columns=["Gate", "Nome", "Status", "Aprovador"],
    )

