import pandas as pd


def compute_descriptive_statistics(stock_df):

    required_columns = [
        "close"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in stock_df.columns
    ]

    if stock_df.empty:
        return pd.DataFrame()

    elif missing_columns:
        return pd.DataFrame()

    elif len(stock_df) < 2:
        return pd.DataFrame()

    # Reverse database order:
    # latest -> oldest becomes oldest -> latest
    df = stock_df.iloc[::-1].copy()

    df["daily_return"] = (
        df["close"]
        .pct_change()
        * 100
    )

    df = df.dropna(subset=["daily_return"])

    if df.empty:
        return pd.DataFrame()

    positive_days = (
        df["daily_return"] > 0
    ).sum()

    negative_days = (
        df["daily_return"] < 0
    ).sum()

    total_days = len(df)

    descriptive_stats = pd.DataFrame(
        {
            "Metric": [
                "Median Close",
                "Median Daily Return",
                "Return Skewness",
                "Return Kurtosis",
                "Positive Trading Days",
                "Negative Trading Days",
            ],
            "Value": [
                f"{df['close'].median():.2f}",
                f"{df['daily_return'].median():.2f}",
                f"{df['daily_return'].skew():.2f}",
                f"{df['daily_return'].kurtosis():.2f}",
                f"{positive_days / total_days * 100:.1f}",
                f"{negative_days / total_days * 100:.1f}",
            ],
            "Unit": [
                "USD",
                "%",
                "Ratio",
                "Ratio",
                "%",
                "%",
            ],
        }
    )

    return descriptive_stats