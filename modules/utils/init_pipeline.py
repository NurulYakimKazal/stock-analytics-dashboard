import streamlit as st
import time


def init_db_and_sync(create_tables, run_etl, sync_interval=21600):

    # -----------------------------
    # 1. Ensure schema exists (run once per session)
    # -----------------------------
    if "db_initialized" not in st.session_state:
        try:
            create_tables()
            st.session_state["db_initialized"] = True
        except Exception as e:
            st.error(f"DB initialization failed: {e}")
            return

    # -----------------------------
    # 2. ETL cooldown logic
    # -----------------------------
    now = time.time()

    last_run = st.session_state.get("last_etl_run")
    is_first_run = last_run is None

    should_run = (
        is_first_run or
        (now - last_run) > sync_interval
    )

    if should_run:
        try:
            with st.spinner("Syncing stock data..."):
                run_etl()

            st.session_state["last_etl_run"] = now
            st.success("Data sync complete")

        except Exception as e:
            # Prevent retrying on every Streamlit rerun after failure
            st.session_state["last_etl_run"] = now
            st.warning(f"Data sync failed: {e}")