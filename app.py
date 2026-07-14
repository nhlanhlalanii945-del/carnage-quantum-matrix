import streamlit as st
import yfinance as yf

# --- Page Layout ---
st.set_page_config(page_title="CRT Terminal", layout="centered")
st.title("⚡ CARNAGE TRADING TERMINAL")

# --- UI Features (The exact selection flow) ---
col1, col2, col3 = st.columns(3)

with col1:
    currency = st.selectbox("Currency", ["ZAR (R)", "USD ($)"])
with col2:
    asset = st.selectbox("Pair/Asset", ["EURUSD", "USDJPY", "GBPUSD", "XAUUSD"])
with col3:
    timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "D1"])

# Mapping for data fetch
ticker_map = {"EURUSD": "EURUSD=X", "USDJPY": "USDJPY=X", "GBPUSD": "GBPUSD=X", "XAUUSD": "GC=F"}
tf_map = {"1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "4h": "1h", "D1": "1d"}

# --- Data Fetch ---
@st.cache_data(ttl=10)
def get_data(sym, tf):
    return yf.download(sym, period="5d", interval=tf, progress=False)

data = get_data(ticker_map[asset], tf_map[timeframe])

if data is not None and len(data) > 5:
    live_price = float(data['Close'].iloc[-1])
    h = float(data['High'].iloc[-5:-1].max())
    l = float(data['Low'].iloc[-5:-1].min())
    
    # CRT Logic: Sweep Detection
    is_bull = live_price < l
    is_bear = live_price > h
    
    # Output Logic
    st.write("---")
    
    # Feature: Metrics Display
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Live Price", f"{live_price:.4f}")
    c2.metric("Entry", f"{live_price:.4f}")
    c3.metric("Stop Loss", f"{l-0.001 if is_bull else h+0.001:.4f}")
    c4.metric("Take Profit", f"{h if is_bull else l:.4f}")
    
    # Feature: Reasoning Card
    st.markdown("### 📋 System Logic Reasoning")
    reasoning = "Market is currently sweeping liquidity. " + ("Bullish setup based on low-range sweep." if is_bull else "Bearish setup based on high-range sweep.")
    st.info(reasoning)

    # Feature: Money Management
    st.markdown("### 🛡️ Risk Management")
    capital = st.number_input(f"Account Capital ({currency.split(' ')[0]})", value=10000.0)
    risk = st.slider("Risk (%)", 0.5, 5.0, 1.0)
    st.success(f"Risk Amount: {currency.split(' ')[0]} {(capital * (risk/100)):,.2f}")

else:
    st.warning("Fetching market data...")
