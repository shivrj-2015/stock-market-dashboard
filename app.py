import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Real-Time Stock Market Dashboard", layout="wide")

st.title("📈 Real-Time Stock Market Dashboard")
st.write("Track live stock data and technical charts with ease.")

# Sidebar Controls
st.sidebar.header("User Input Settings")
ticker_symbol = st.sidebar.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, RELIANCE.NS)", "AAPL")
period = st.sidebar.selectbox("Select Time Horizon", ["1d", "5d", "1mo", "6mo", "1y", "5y", "max"], index=4)

# Fetching Data
try:
    stock = yf.Ticker(ticker_symbol)
    df = stock.history(period=period)
    info = stock.info

    if not df.empty:
        # Display Stock Overview Metrics
        col1, col2, col3, col4 = st.columns(4)
        current_price = df['Close'].iloc[-1]
        prev_close = df['Close'].iloc[-2] if len(df) > 1 else current_price
        price_change = current_price - prev_close
        pct_change = (price_change / prev_close) * 100

        col1.metric("Current Price", f"${current_price:.2f}", f"{price_change:+.2f} ({pct_change:+.2f}%)")
        col2.metric("Company", info.get("shortName", ticker_symbol))
        col3.metric("52-Week High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
        col4.metric("52-Week Low", f"${info.get('fiftyTwoWeekLow', 'N/A')}")

        # Candlestick Chart
        st.subheader("Price Trend (Candlestick Chart)")
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name="Candlestick"
        )])
        fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark", height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Raw Data Table
        with st.expander("View Raw Historical Data"):
            st.dataframe(df.tail(10))
    else:
        st.error("No data found for this ticker symbol. Please try another one (e.g., AAPL, TSLA).")

except Exception as e:
    st.error(f"Error fetching data: {e}")