def compute_stock_time_range(df):
    return {
        "earliest_date": df["date"].min().date(),
        "latest_date": df["date"].max().date(),
    }