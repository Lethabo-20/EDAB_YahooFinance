import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta

st.title("Multi-Stock Time Series Visualization")

# Default date range: last 6 months
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

        # If only one ticker, fetch without multi-index
        multiple = len(tickers) > 1
        st.info("Fetching data...")

        data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', auto_adjust=True)

        if data.empty:
            st.warning("No data found.")
        else:
            combined_data = []

            for ticker in tickers:
                try:
                    if multiple:
                        ticker_df = data[ticker][["Close"]].copy()
                    else:
                        ticker_df = data[["Close"]].copy()
                    ticker_df["Ticker"] = ticker
                    ticker_df["Date"] = ticker_df.index
                    combined_data.append(ticker_df.reset_index(drop=True))
                except KeyError:
                    st.warning(f"No data found for {ticker}")

            if not combined_data:
                st.error("None of the tickers had valid data.")
            else:
                final_df = pd.concat(combined_data, ignore_index=True)

                # Show Table
                st.write("📄 Combined Data Table")
                st.dataframe(final_df)

                # Plot
                fig, ax = plt.subplots(figsize=(12, 6))
                for ticker in final_df["Ticker"].unique():
                    ticker_data = final_df[final_df["Ticker"] == ticker]
                    ax.plot(ticker_data["Date"], ticker_data["Close"], label=ticker)
                ax.set(title="Stock Closing Prices", xlabel="Date", ylabel="Price (USD)")
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)

                # Download button
                csv = final_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="multi_stock_data.csv",
                    mime="text/csv"
                )
