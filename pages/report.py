import streamlit as st

from modules.charts.cumulative_return_chart import plot_cumulative_return
from modules.charts.trend_indicators_chart import plot_trend_indicators
from modules.kpis.stock_explorer_kpis import compute_stock_explorer_kpis
from modules.kpis.performance_overview_kpis import compute_performance_overview_kpis
from modules.kpis.risk_analysis_kpis import compute_risk_analysis_kpis
from modules.reports.descriptive_statistics import compute_descriptive_statistics
from components.footer import render_footer

from modules.utils.spacer import spacer
from modules.reports.pdf_report import generate_pdf_report



# =========================================================
# STOCK REPORT
# =========================================================

def show_stock_report(
    company_kpis,
    performance_kpis,
    risk_kpis,
    descriptive_stats,
    stock_df,
):

    st.title("📄 Stock Report")


    # =========================================================
    # COMPANY OVERVIEW
    # =========================================================

    spacer(1)

    company = company_kpis["company"]

    st.header(
        f"{company['name']} ({company['ticker']})"
    )

    st.caption(
        f"{company['sector']} • {company['industry']}"
    )


    spacer(2)


    # =========================================================
    # MARKET SNAPSHOT
    # =========================================================

    st.subheader("Market Snapshot")

    col1, col2, col3, col4 = st.columns(
        4,
        border=True,
    )

    with col1:
        st.metric(
            "Market Cap",
            company_kpis["market_cap"],
        )

    with col2:
        st.metric(
            "P/E Ratio",
            company_kpis["trailing_pe"],
        )

    with col3:
        st.metric(
            "Dividend Yield",
            company_kpis["dividend"],
        )

    with col4:
        st.metric(
            "Beta",
            company_kpis["beta"],
        )


    spacer(2)


    # =========================================================
    # PERFORMANCE ANALYSIS
    # =========================================================

    st.subheader("Performance Summary")

    col1, col2, col3 = st.columns(
        3,
        border=True,
    )

    with col1:
        st.metric(
            "Total Return",
            performance_kpis["total_return"],
        )

    with col2:
        st.metric(
            "Highest Close",
            performance_kpis["highest_close"],
        )

    with col3:
        st.metric(
            "Lowest Close",
            performance_kpis["lowest_close"],
        )

    spacer(2)


    st.subheader("Cumulative Return")

    cumulative_return_fig = plot_cumulative_return(
        stock_df
    )


    spacer(2)


    # =========================================================
    # RISK ANALYSIS
    # =========================================================

    st.subheader("Risk Summary")

    col1, col2, col3 = st.columns(
        3,
        border=True,
    )

    with col1:
        st.metric(
            "Volatility",
            risk_kpis["volatility"],
        )

    with col2:
        st.metric(
            "Annualized Volatility",
            risk_kpis["annualized_volatility"],
        )

    with col3:
        st.metric(
            "Maximum Drawdown",
            risk_kpis["maximum_drawdown"],
        )

    col1, col2 = st.columns(
        2,
        border=True,
    )

    with col1:
        st.metric(
            "Best Trading Day",
            risk_kpis["best_trading_day"],
        )

    with col2:
        st.metric(
            "Worst Trading Day",
            risk_kpis["worst_trading_day"],
        )


    spacer(2)

    # =========================================================
    # TREND ANALYSIS
    # =========================================================

    st.subheader("Trend Overview")

    trend_fig = plot_trend_indicators(
        stock_df
    )


    spacer(2)

    # =========================================================
    # DESCRIPTIVE STATISTICS
    # =========================================================

    st.subheader("Descriptive Statistics")

    if descriptive_stats.empty:
        st.info(
            "No descriptive statistics available."
        )
    else:
        st.dataframe(
            descriptive_stats,
            width="stretch",
            hide_index=True,
        )

    spacer(2)

    return {
        "cumulative_return": cumulative_return_fig,
        "trend": trend_fig,
    }

# =========================================================
# PAGE EXECUTION
# =========================================================

company_df = st.session_state.get("company_df")
stock_dataframe = st.session_state.get("stock_df")

start_date = st.session_state.get("start_date")
end_date = st.session_state.get("end_date")


if (
    company_df is None
    or stock_dataframe is None
    or start_date is None
    or end_date is None
):
    st.warning(
        "Stock data or date range is unavailable. Please select a ticker first."
    )
    st.stop()

company_kpis_data = compute_stock_explorer_kpis(
    company_df
)

performance_kpis_data = compute_performance_overview_kpis(
    stock_dataframe
)

risk_kpis_data = compute_risk_analysis_kpis(
    stock_dataframe
)

descriptive_stats_data = compute_descriptive_statistics(
    stock_dataframe
)

charts = show_stock_report(
    company_kpis_data,
    performance_kpis_data,
    risk_kpis_data,
    descriptive_stats_data,
    stock_dataframe
)

# =========================================================
# PDF EXPORT
# =========================================================

pdf_bytes = generate_pdf_report(
    company_kpis_data,
    performance_kpis_data,
    risk_kpis_data,
    descriptive_stats_data,
    charts,
    start_date,
    end_date,
)


st.download_button(
    label="Download PDF Report",
    data=pdf_bytes,
    file_name=f"{company_kpis_data['company']['ticker']}_stock_report.pdf",
    mime="application/pdf",
)

render_footer()