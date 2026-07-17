import streamlit as st
from modules.utils.spacer import spacer
from modules.kpis.performance_overview_kpis import compute_performance_overview_kpis
from modules.kpis.risk_analysis_kpis import compute_risk_analysis_kpis
from modules.charts.cumulative_return_chart import plot_cumulative_return
from modules.charts.return_analysis_charts import plot_return_histogram, plot_daily_returns
from modules.charts.trend_indicators_chart import plot_trend_indicators
from modules.charts.volume_activity_chart import plot_volume_activity
from modules.utils.no_data_warning import show_no_stock_data_warning
from modules.reports.descriptive_statistics import compute_descriptive_statistics
from components.footer import render_footer


def analytics(company_df, stock_df, performance_kpis, risk_kpis):

    company = company_df.iloc[0]

    st.title("📈 Analytics")

    spacer(1)

    # =========================================================
    # COMPANY SUMMARY
    # =========================================================

    st.header(f"{company['name']} ({company['ticker']})")
    st.caption(f"{company['sector']} • {company['industry']}")

    spacer(2)

    # =========================================================
    # PERFORMANCE OVERVIEW
    # =========================================================

    st.subheader("Performance Overview")

    col1, col2, col3 = st.columns(3, border=True)

    with col1:
        st.metric(
            "Total Return",
            performance_kpis["total_return"],
        )

    with col2:
        st.metric(
            "Average Daily Return",
            performance_kpis["avg_daily_return"],
        )


    with col3:
        st.metric(
            "Average Daily Volume",
            performance_kpis["avg_volume"],
        )

    spacer(1)

    col1, col2, col3 = st.columns(3, border=True)

    with col1:
        st.metric(
            "Trading Days",
            performance_kpis["trading_days"],
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

    # =========================================================
    # PRICE PERFORMANCE
    # =========================================================

    st.subheader("Cumulative Return")

    if stock_df.empty:
        show_no_stock_data_warning()
    else:
        plot_cumulative_return(stock_df)     # Plot normalized price / cumulative return

    spacer(2)

    # =========================================================
    # RETURN ANALYSIS
    # =========================================================

    st.subheader("Return Analysis")

    col1, col2 = st.columns(2)

    with col1:
        plot_daily_returns(stock_df)

    with col2:
        plot_return_histogram(stock_df)

    spacer(2)

    # =========================================================
    # RISK ANALYSIS
    # =========================================================

    st.subheader("Risk Analysis")

    col1, col2, col3 = st.columns(3, border=True)

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

    spacer(1)

    col1, col2 = st.columns(2, border=True)

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
    # TREND INDICATORS
    # =========================================================

    st.subheader("Trend Indicators")

    if stock_df.empty:
        show_no_stock_data_warning()
    else:
        plot_trend_indicators(stock_df)     # Moving averages

    spacer(2)

    # =========================================================
    # VOLUME ANALYSIS
    # =========================================================

    st.subheader("Volume Activity")

    if stock_df.empty:
        show_no_stock_data_warning()
    else:
        plot_volume_activity(stock_df)      # Volume chart

    spacer(2)

    # =========================================================
    # DESCRIPTIVE STATISTICS
    # =========================================================

    with st.expander("Descriptive Statistics", expanded=True):
        descriptive_stats = compute_descriptive_statistics(stock_df)

        if descriptive_stats.empty:
            st.warning("No descriptive statistics available.")
        else:
            st.dataframe(
                descriptive_stats,
                width="stretch",
                hide_index=True,
            )

    render_footer()




company_dataframe = st.session_state.company_df
stock_dataframe = st.session_state.stock_df

performance_kpis_value = compute_performance_overview_kpis(stock_dataframe)
risk_kpis_value = compute_risk_analysis_kpis(stock_dataframe)

analytics(
    company_dataframe,
    stock_dataframe,
    performance_kpis_value,
    risk_kpis_value
)