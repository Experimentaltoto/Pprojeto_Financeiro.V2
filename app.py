"""Protótipo de dashboard de vendas.

Lê o CSV normalizado pelo `finance_normalizer` (fonte Stone) e apresenta um
recorte de vendas em cartão. É um protótipo de visualização: ainda não lê do
Supabase, conforme definido no PRD para a versão final.
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent / "src"))
from finance_normalizer.normalizer import normalize_file  # noqa: E402

ROOT = Path(__file__).parent
RAW_STONE = ROOT / "Dados" / "Vendas_Stone_Set.xlsx"
NORMALIZED_SALES = ROOT / "saida" / "vendas.csv"

st.set_page_config(page_title="Vendas (protótipo)", layout="wide")
st.title("Vendas — protótipo")


def gerar_csv() -> None:
    NORMALIZED_SALES.parent.mkdir(parents=True, exist_ok=True)
    count = normalize_file(RAW_STONE, NORMALIZED_SALES, source="stone")
    st.success(f"{count} vendas normalizadas a partir de {RAW_STONE.name}.")


def fmt_brl(valor: Decimal) -> str:
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {texto}"


if st.button("Atualizar dados da Stone"):
    gerar_csv()

if not NORMALIZED_SALES.exists():
    gerar_csv()

df = pd.read_csv(NORMALIZED_SALES, dtype=str)
df = df[df["record_type"] == "card_sale"].copy()

if df.empty:
    st.warning("Nenhuma venda encontrada no arquivo normalizado.")
    st.stop()

for coluna in ("gross_amount", "fee_amount", "net_amount"):
    df[coluna] = df[coluna].apply(lambda v: Decimal(v) if v else Decimal("0"))

df["data_venda"] = pd.to_datetime(df["competence_date"])

data_min, data_max = df["data_venda"].min().date(), df["data_venda"].max().date()
periodo = st.date_input("Período", (data_min, data_max), min_value=data_min, max_value=data_max)
if isinstance(periodo, tuple) and len(periodo) == 2:
    inicio, fim = periodo
    df = df[(df["data_venda"] >= pd.Timestamp(inicio)) & (df["data_venda"] <= pd.Timestamp(fim))]

status_disponiveis = sorted(df["status"].unique())
status_selecionados = st.multiselect("Status", status_disponiveis, default=status_disponiveis)
df = df[df["status"].isin(status_selecionados)]

total_bruto = sum(df["gross_amount"], Decimal("0"))
total_liquido = sum(df["net_amount"], Decimal("0"))
total_taxas = sum(df["fee_amount"], Decimal("0"))
qtd_vendas = len(df)
ticket_medio = (total_bruto / qtd_vendas) if qtd_vendas else Decimal("0")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Faturamento bruto", fmt_brl(total_bruto))
c2.metric("Recebimento líquido", fmt_brl(total_liquido))
c3.metric("Taxas de cartão", fmt_brl(total_taxas))
c4.metric("Qtd. de vendas", qtd_vendas)
c5.metric("Ticket médio", fmt_brl(ticket_medio))

st.subheader("Evolução diária")
diario = (
    df.groupby(df["data_venda"].dt.date)
    .agg(
        bruto=("gross_amount", lambda s: float(sum(s, Decimal("0")))),
        liquido=("net_amount", lambda s: float(sum(s, Decimal("0")))),
    )
    .reset_index()
    .rename(columns={"data_venda": "data"})
)
st.line_chart(diario, x="data", y=["bruto", "liquido"])

st.subheader("Vendas por status")
por_status = df.groupby("status").size().reset_index(name="quantidade")
st.bar_chart(por_status, x="status", y="quantidade")

st.subheader("Lançamentos detalhados")
tabela = df[["data_venda", "description", "status", "gross_amount", "fee_amount", "net_amount"]].copy()
for coluna in ("gross_amount", "fee_amount", "net_amount"):
    tabela[coluna] = tabela[coluna].astype(float)
tabela["data_venda"] = tabela["data_venda"].dt.strftime("%d/%m/%Y")
tabela = tabela.rename(columns={
    "data_venda": "Data",
    "description": "Descrição",
    "status": "Status",
    "gross_amount": "Bruto (R$)",
    "fee_amount": "Taxas (R$)",
    "net_amount": "Líquido (R$)",
})
st.dataframe(tabela.sort_values("Data"), width="stretch", hide_index=True)
