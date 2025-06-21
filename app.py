import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta

st.title("Stock Time Series Visualization")

# Default dates
default_end = date.today()
default_start = default_end - timedelta(days=180)

# Inputs
tickers_input = st.text_input("Enter stock ticker:")
start_date = st.date_input("Start Date", value=default_start)
end_date = st.date_input("End Date", value=default_end)

if st.button("Fetch Data"):
    if not tickers_input.strip():
        st.error("Please enter at least one stock ticker.")
    elif start_date >= end_date:
        st.error("Start date must be before end date.")
    else:
        tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]
        all_data = {}

        for ticker in tickers:
            df = yf.download(ticker, start=start_date, end=end_date)
            if df.empty:
                st.warning(f"No data found for {ticker}")
            else:
                df["Ticker"] = ticker
                all_data[ticker] = df

        if all_data:
            combined_df = pd.concat(all_data.values())

            # Show raw data
            st.write("📄 Data Preview")
            st.dataframe(combined_df.tail())

            # Plot
            fig, ax = plt.subplots(figsize=(12, 6))
            for ticker, df in all_data.items():
                ax.plot(df.index, df["Close"], label=ticker)
            ax.set(title="Stock Closing Prices", xlabel="Date", ylabel="Price (USD)")
            ax.legend()
            ax.grid(True)

            st.pyplot(fig)

            # Download button
            csv = combined_df.to_csv().encode("utf-8")
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="stock_data.csv",
                mime="text/csv"
            )
        else:
            st.error("No valid data fetched for any of the entered tickers.")
