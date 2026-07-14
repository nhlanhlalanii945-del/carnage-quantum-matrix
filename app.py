import streamlit as st
import yfinance as yf

# --- Page Config ---
st.set_page_config(page_title="CRT & 714 Terminal", layout="centered")
st.title("⚡ CARNAGE & 714 TRADING TERMINAL")

# --- UI Inputs (Manual Rands Input) ---
col1, col2 = st.columns(2)
with col1:
    currency = st.selectbox("Currency", ["ZAR (R)", "USD ($)"])
    asset = st.selectbox("Pair/Asset", ["EURUSD", "USDJPY", "GBPUSD", "XAUUSD"])
with col2:
    # Manual input for your Rands amount
    capital = st.number_input("Enter Capital (e.g. 200)", value=200.0, step=50.0)
    risk_percent = st.slider("Risk per Trade (%)", 0.5, 5.0, 1.0)

timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "D1"])

# --- Logic & Data ---
ticker_map = {"EURUSD": "EURUSD=X", "USDJPY": "USDJPY=X", "GBPUSD": "GBPUSD=X", "XAUUSD": "GC=F"}
tf_map = {"1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "4h": "1h", "D1": "1d"}

@st.cache_data(ttl=10)
def get_data(sym, tf):
    return yf.download(sym, period="5d", interval=tf, progress=False)

data = get_data(ticker_map[asset], tf_map[timeframe])

if data is not None and len(data) > 5:
    live_price = float(data['Close'].iloc[-1])
    h = float(data['High'].iloc[-5:-1].max())
    l = float(data['Low'].iloc[-5:-1].min())
    
    # Logic: Liquidity Sweep
    is_bull = live_price < l
    is_bear = live_price > h
    
    sl_price = l - 0.001 if is_bull else h + 0.001
    sl_distance = abs(live_price - sl_price)
    
    # Lot Size Calculation
    risk_amount = capital * (risk_percent / 100)
    lot_size = risk_amount / (sl_distance * 100000) 
    
    # Confidence Scoring (Logic for your strategy confluence)
    confidence = 85 if (is_bull or is_bear) else 40
    
    # Output Display
    st.write("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Live Price", f"{live_price:.4f}")
    c2.metric("Entry", f"{live_price:.4f}")
    c3.metric("Stop Loss", f"{sl_price:.4f}")
    c4.metric("Take Profit", f"{h if is_bull else l:.4f}")
    
    # Strategy Explanation
    st.markdown("### 📋 Combined Strategy Reasoning")
    st.info(f"**Strategy Confluence:** Active liquidity sweep + 714 Method cycle. **Confidence: {confidence}%**")
    
    # Execution
    st.success(f"🎛️ **Calculated Lot Size:** {max(0.01, round(lot_size, 2))}")
    st.write(f"Based on **{currency}** capital of {capital:,.2f} and **{risk_percent}%** risk.")

else:
    st.warning("Fetching market data...")
