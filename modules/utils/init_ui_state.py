import streamlit as st

from src.etl.config import TICKERS


def init_ui_state(stats, ticker):

    earliest = stats["earliest_date"]
    latest = stats["latest_date"]

    defaults = {
        "ticker": TICKERS[0],
        "company_df": None,
        "stock_df": None,
        "loaded_ticker": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


    # =========================
    # RESET DATE RANGE ON TICKER CHANGE
    # =========================

    if st.session_state["loaded_ticker"] != ticker:

        st.session_state["date_range"] = (
            earliest,
            latest,
        )

        st.session_state["loaded_ticker"] = ticker