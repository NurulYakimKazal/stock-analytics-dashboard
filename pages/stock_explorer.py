import streamlit as st

from modules.charts.historical_price_chart import plot_historical_price
from modules.kpis.stock_explorer_kpis import compute_stock_explorer_kpis
from modules.utils.spacer import spacer
from modules.utils.no_data_warning import show_no_stock_data_warning
from components.footer import render_footer


def stock_explorer(stock_df, stock_kpis):

    st.title("📊 Stock Explorer")

    spacer(1)

    # =========================================================
    # COMPANY HEADER
    # =========================================================
    company = stock_kpis["company"]

    st.header(f"{company['name']} ({company['ticker']})")
    st.caption(f"{company['sector']} • {company['industry']}")


    spacer(2)

    # =========================================================
    # KEY METRICS
    # =========================================================

    col1, col2, col3, col4 = st.columns(4, border=True)

    with col1:
        st.metric(
            "Market Cap",
            stock_kpis["market_cap"],
        )

    with col2:
        st.metric(
            "P/E Ratio",
            stock_kpis["trailing_pe"]
        )

    with col3:
        st.metric(
            "Dividend Yield",
            stock_kpis["dividend"],
        )

    with col4:
        st.metric(
            "Beta",
            stock_kpis["beta"],
        )

    spacer(2)

    # =========================================================
    # PRICE CHART
    # =========================================================

    st.subheader("Historical Price")

    if stock_df.empty:
        show_no_stock_data_warning()
    else:
        plot_historical_price(stock_df)

    spacer(2)

    # =========================================================
    # PRICE TABLE
    # =========================================================

    with st.expander("Historical Price Data"):
        if stock_df.empty:
            show_no_stock_data_warning()
        else:
            st.dataframe(
                stock_df.drop(columns='ticker'),
                width='stretch',
                hide_index=True,
            )

    render_footer()



company_data = st.session_state.company_df
stock_data = st.session_state.stock_df

stock_explorer_kpis = compute_stock_explorer_kpis(company_data)

stock_explorer(stock_data, stock_explorer_kpis)

