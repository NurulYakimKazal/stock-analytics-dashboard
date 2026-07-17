import streamlit as st
from datetime import datetime

from src.etl.config import TICKERS


def render_ticker():

    st.sidebar.title("Filters")

    return st.sidebar.selectbox(
        "Ticker",
        TICKERS,
        key="ticker",
    )


def render_date_range(stats):

    min_date = stats["earliest_date"]
    max_date = stats["latest_date"]

    date_range = st.sidebar.date_input(
        "Date range",
        min_value=min_date,
        max_value=max_date,
        key="date_range",
    )

    # SAFE PARSING
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range

        # Save the last complete range
        st.session_state["last_valid_date_range"] = (
            start_date,
            end_date,
        )
    else:
        start_date, end_date = st.session_state.get(
            "last_valid_date_range",
            (min_date, max_date),
        )

    start_time = datetime.combine(
        start_date,
        datetime.min.time()
    )

    end_time = datetime.combine(
        end_date,
        datetime.max.time()
    )

    return {
        "start_time": start_time,
        "end_time": end_time,
    }
