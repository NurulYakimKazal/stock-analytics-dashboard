import streamlit as st
import plotly.graph_objects as go


def plot_volume_activity(stock_df):

    required_columns = ["date", "volume"]

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

    if len(df) < 20:
        st.info(
            "Less than 20 trading days available. "
            "Average volume line may be incomplete."
        )

    df["average_volume"] = (
        df["volume"]
        .rolling(window=20)
        .mean()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["volume"],
            name="Daily Volume",
            marker=dict(
                color="#636EFA",
            ),
            hovertemplate=(
                "Volume: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["average_volume"],
            mode="lines",
            name="20-Day Average Volume",
            line=dict(
                color="#EF553B",
                width=2,
            ),
            hovertemplate=(
                "20-Day Avg: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Volume",
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