import streamlit as st

from src.etl.config import TICKERS


def init_ui_state(stats):

    earliest = stats["earliest_date"]
    latest = stats["latest_date"]

    # =========================
    # DEFAULT STATE INITIALIZATION
    # =========================
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
        # SAFE DATE STATE NORMALIZATION
        # =========================
        if "date_range" not in st.session_state:
            st.session_state["date_range"] = (earliest, latest)

        else:
            raw = st.session_state["date_range"]

            if isinstance(raw, tuple) and len(raw) == 2:
                start, end = raw

                start = max(start, earliest)
                end = min(end, latest)

                if start <= end:
                    st.session_state["date_range"] = (start, end)
                else:
                    st.session_state["date_range"] = (end, start)