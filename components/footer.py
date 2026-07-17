import streamlit as st


def render_footer():

    st.divider()

    st.caption(
        """
        Data Source: Yahoo Finance (`yfinance`)  
        Historical stock prices, trading volume, and company information are retrieved through the 
        `yfinance` Python library. Data availability and accuracy are subject to Yahoo Finance services.
        """
    )