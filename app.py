import streamlit as st
import pandas as pd

from src.etl.stock_incremental_etl import run_stock_etl
from src.db.stock_database import create_stock_tables
from modules.utils.init_pipeline import init_db_and_sync

from components.sidebar import render_ticker, render_date_range
from src.etl.config import TICKERS
from src.db.stock_database import fetch_stock_data
from src.db.company_database import fetch_company_data
from modules.utils.compute_stock_time_range import compute_stock_time_range
from modules.utils.init_ui_state import init_ui_state


st.set_page_config(
    page_title="Stock Dashboard",
    layout="wide",
)


# -----------------------------
# INITIALIZATION
# -----------------------------
init_db_and_sync(
    create_stock_tables,
    run_stock_etl
)


# =========================
# DEFAULT TICKER
# =========================

if "ticker" not in st.session_state:
    st.session_state["ticker"] = TICKERS[0]


# =========================
# SELECT TICKER
# =========================

ticker = render_ticker()


# =========================
# FETCH DATA ONCE
# =========================

company_df = fetch_company_data(ticker)
stock_df = fetch_stock_data(ticker)


# =========================
# COMPUTE STATS
# =========================

stats = compute_stock_time_range(stock_df)

init_ui_state(stats)


# =========================
# DATE FILTER
# =========================

date_range = render_date_range(stats)

start_date = date_range['start_time']
end_date = date_range['end_time']

stock_df = stock_df[
    stock_df["date"].between(
        pd.Timestamp(start_date),
        pd.Timestamp(end_date),
    )
]

# =========================
# STORE SELECTED DATE RANGE
# =========================

st.session_state.start_date = start_date
st.session_state.end_date = end_date

# =========================
# SHARE DATA
# =========================
st.session_state.stock_df = stock_df
st.session_state.company_df = company_df


# -----------------------------
# NAVIGATION
# -----------------------------

pg = st.navigation(
    [
        st.Page(
            "pages/stock_explorer.py",
            title="Stock Explorer",
            icon=":material/dashboard:",
            default=True,
        ),
        st.Page(
            "pages/analytics.py",
            title="Analytics",
            icon=":material/analytics:",
        ),
        st.Page(
            "pages/report.py",
            title="Report",
            icon=":material/description:",
        ),
    ]
)

pg.run()