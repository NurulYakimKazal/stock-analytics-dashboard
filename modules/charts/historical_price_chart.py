import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_historical_price(df):

    required_columns = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if df.empty:
        st.info("No stock data available.")
        return

    elif missing_columns:
        st.warning(
            f"Missing stock data: {', '.join(missing_columns)}"
        )
        return

    # Reverse database order:
    # latest → oldest becomes oldest → latest
    df = df.iloc[::-1].copy()


    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25],
    )


    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df["date"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Price",
            hovertemplate=(
                "Date: %{x}<br>"
                "Open: $%{open:.2f}<br>"
                "High: $%{high:.2f}<br>"
                "Low: $%{low:.2f}<br>"
                "Close: $%{close:.2f}"
                "<extra></extra>"
            ),
        ),
        row=1,
        col=1,
    )


    # Volume
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["volume"],
            name="Volume",
            marker=dict(
                color="#636EFA"
            ),
            hovertemplate=(
                "Date: %{x}<br>"
                "Volume: %{y:,.0f}"
                "<extra></extra>"
            ),
        ),
        row=2,
        col=1,
    )


    fig.update_layout(
        height=700,
        xaxis_rangeslider_visible=False,
        showlegend=False,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
    )


    fig.update_yaxes(
        title_text="Price",
        row=1,
        col=1,
    )

    fig.update_yaxes(
        title_text="Volume",
        row=2,
        col=1,
    )


    st.plotly_chart(
        fig,
        width="stretch",
    )

    return fig