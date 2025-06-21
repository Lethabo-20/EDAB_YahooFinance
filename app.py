import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta

st.title("Multi-Stock Time Series Visualization")

# Default dates
default_end = date.today()
default_start = default_end - timedelta(days=180)

# Inputs
tickers_input = st.text_input("Enter stock tickers (comma-separated, e.g., AAPL, MSFT, NVDA):")
start_date = st.date_input("Start Date", value=default_start)
end_date = st.date_input("End Date", value=default_end)

if st.button("Fetch Data"):
    if not tickers_input.strip():
        st.error("Please enter at least one stock ticker.")
    elif start_date >= end_date:
        st.error("Start date must be before end date.")
    else:
        tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]
        combined_df = pd.DataFrame()

        st.info("Fetching data...")

        for ticker in tickers:
            df = yf.download(ticker, start=start_date, end=end_date)
            if df.empty:
                st.warning(f"No data for {ticker}")
                continue
            df = df[["Close"]]  # Only keep Close price
            df["Ticker"] = ticker
            df["Date"] = df.index
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        if not combined_df.empty:
            # Plot each ticker separately
            fig, ax = plt.subplots(figsize=(12, 6))
            for ticker in combined_df["Ticker"].unique():
                ticker_data = combined_df[combined_df["Ticker"] == ticker]
                ax.plot(ticker_data["Date"], ticker_data["Close"], label=ticker)
            ax.set(title="Stock Closing Prices", xlabel="Date", ylabel="Price (USD)")
            ax.legend()
            ax.grid(True)

            st.pyplot(fig)

            # Show combined table
            st.write("📄 Combined Data Table")
            st.dataframe(combined_df)

            # Download CSV
            csv = combined_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="multi_stock_data.csv",
                mime="text/csv"
            )
        else:
            st.error("No data fetched for any valid tickers.")
