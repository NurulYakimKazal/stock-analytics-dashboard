import streamlit as st
import plotly.graph_objects as go


def plot_trend_indicators(stock_df):

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

    if len(df) < 50:
        st.info(
            "Less than 50 trading days available. "
            "Moving average lines may be incomplete."
        )

    df["MA20"] = (
        df["close"]
        .rolling(window=20)
        .mean()
    )

    df["MA50"] = (
        df["close"]
        .rolling(window=50)
        .mean()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["close"],
            name="Close Price",
            line=dict(
                color="#636EFA",
                width=2,
            ),
            hovertemplate=(
                "Close: $%{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["MA20"],
            name="20-Day MA",
            line=dict(
                color="#EF553B",
                width=2,
            ),
            hovertemplate=(
                "MA-20: $%{y:.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["MA50"],
            name="50-Day MA",
            line=dict(
                color="#00CC96",
                width=2,
            ),
            hovertemplate=(
                "MA-50: $%{y:.2f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        height=400,
        hovermode="x unified",
        margin=dict(
            t=20,
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