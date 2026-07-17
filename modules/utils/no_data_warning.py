import streamlit as st


def show_no_stock_data_warning():
    st.warning("No stock data available for the selected ticker and date range.")