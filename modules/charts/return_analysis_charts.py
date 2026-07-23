import streamlit as st
import plotly.graph_objects as go


def plot_daily_returns(stock_df):

    required_columns = ["date", "close"]

    missing_columns = [
        col for col in required_columns
        if col not in stock_df.columns
    ]

    if stock_df.empty:
        st.info("No stock data available.")
        return

    elif missing_columns:
        st.warning(
            f"Missing stock data: {', '.join(missing_columns)}"
        )
        return

    df = stock_df.iloc[::-1].copy()

    df["daily_return"] = (
            df["close"]
            .pct_change()
            * 100
    )

    df = df.dropna()

    if df.empty:
        st.info(
            "At least two trading days are required to calculate daily returns."
        )
        return

    df["color"] = df["daily_return"].apply(
        lambda x: "#00CC96" if x >= 0 else "#EF553B"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["daily_return"],
            marker_color=df["color"],
            name="Daily Return",
            hovertemplate=(
                "Return: %{y:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
    )

    fig.update_layout(
        title="Daily Return Over Time",
        xaxis_title="Date",
        yaxis_title="Daily Return (%)",
        height=350,
        showlegend=False,
        hovermode="x unified",
        margin=dict(
            t=50,
            l=20,
            r=20,
            b=20,
        ),
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

    return fig


def plot_return_histogram(stock_df):

    required_columns = ["close"]

    missing_columns = [
        col for col in required_columns
        if col not in stock_df.columns
    ]

    if stock_df.empty:
        st.info("No stock data available.")
        return

    elif missing_columns:
        st.warning(
            f"Missing stock data: {', '.join(missing_columns)}"
        )
        return

    df = stock_df.iloc[::-1].copy()

    df["daily_return"] = (
            df["close"]
            .pct_change()
            * 100
    )

    df = df.dropna(subset=["daily_return"])

    if df.empty:
        st.info(
            "At least two trading days are required to calculate return distribution."
        )
        return

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=df["daily_return"],
            nbinsx=40,
            name="Daily Return",
            marker=dict(
                color="#636EFA"
            ),
            hovertemplate=(
                "Return: %{x:.2f}%<br>"
                "Frequency: %{y}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_vline(
        x=df["daily_return"].mean(),
        line_dash="dash",
        line_color="red",
        annotation_text="Average",
    )

    fig.update_layout(
        title="Return Distribution",
        xaxis_title="Daily Return (%)",
        yaxis_title="Frequency",
        height=350,
        showlegend=False,
        margin=dict(
            t=50,
            l=20,
            r=20,
            b=20,
        ),
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

    return fig