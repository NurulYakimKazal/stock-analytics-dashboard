import streamlit as st
import pandas as pd


def compute_stock_explorer_kpis(company_df):
    required_columns = [
        "name",
        "ticker",
        "sector",
        "industry",
        "market_cap",
        "trailing_pe",
        "dividend_yield",
        "beta"
    ]

    missing_columns = [col for col in required_columns if col not in company_df.columns]

    default_values = {
        "company": {
            "name": "N/A",
            "ticker": "N/A",
            "sector": "N/A",
            "industry": "N/A",
        },
        "market_cap": "N/A",
        "trailing_pe": "N/A",
        "dividend": "N/A",
        "beta": "N/A",
    }

    if company_df.empty:
        st.warning("No company information found.")
        return default_values

    elif missing_columns:
        st.warning(f"Missing company information: {', '.join(missing_columns)}")
        return default_values

    else:
        company = company_df.iloc[0].to_dict()

        market_cap_value = company["market_cap"]
        market_cap = (
            "N/A"
            if pd.isna(market_cap_value)
            else f"${market_cap_value / 1_000_000_000_000:.2f}T"
            if market_cap_value >= 1_000_000_000_000
            else f"${market_cap_value / 1_000_000_000:.2f}B"
            if market_cap_value >= 1_000_000_000
            else f"${market_cap_value / 1_000_000:.2f}M"
            if market_cap_value >= 1_000_000
            else f"${market_cap_value:,.0f}"
        )

        pe_value = company["trailing_pe"]
        trailing_pe = f"{pe_value:.2f}" if pd.notna(pe_value) else "N/A"

        dividend_value = company["dividend_yield"]
        dividend = f"{dividend_value:.2f}%" if pd.notna(dividend_value) else "N/A"

        beta_value = company["beta"]
        beta = f"{beta_value:.2f}" if pd.notna(beta_value) else "N/A"

    return {
        "company": company,
        "market_cap": market_cap,
        "trailing_pe": trailing_pe,
        "dividend": dividend,
        "beta": beta
    }