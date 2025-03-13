import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# Stock dictionary
STOCKS = {
    "Alphabet (GOOGL)": "GOOGL",
    "Nvidia (NVDA)": "NVDA",
    "Microsoft (MSFT)": "MSFT"
}

st.title("Stock Time Series Visualization")

# User inputs
selected_stock = st.selectbox("Choose a stock:", STOCKS)
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Fetch Data"):
    df = yf.download(STOCKS[selected_stock], start=start_date, end=end_date)

    if df.empty:
        st.warning("No data available for the selected period.")
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df.index, df["Close"], label="Closing Price", color="blue")
        ax.set(title=f"{selected_stock} Stock Prices", xlabel="Date", ylabel="Price (USD)")
        ax.legend()
        ax.grid()

        st.pyplot(fig)
