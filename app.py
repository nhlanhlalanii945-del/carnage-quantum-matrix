import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- App Config ---
st.set_page_config(page_title="CRT Cloud Terminal", layout="wide")
st.title("⚡ CARNAGE TRADING TERMINAL (CRT Edition)")
st.write("---")

# --- CSS Styling Injection ---
st.markdown("""
    <style>
    .stMetric {
        background-color: #1e1e1e;
        border: 1px solid #333333;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True) # <-- Corrected argument to prevent TypeErrors

# --- UI Inputs (Rands & Timeframes) ---
st.sidebar.header("🛠️ Core Configuration")

# Mapping assets to cloud-friendly Yahoo Finance tick markers
asset_map = {
    "XAUUSD (Gold Spot)": "GC=F",
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "GBPJPY": "GBPJPY=X"
}
selected_asset = st.sidebar.selectbox("Target Asset", list(asset_map.keys()))
ticker_symbol = asset_map[selected_asset]

# Interval Configuration
ltf_interval = st.sidebar.selectbox("Execution TF (Lower Timeframe)", ["1m", "5m", "15m", "1h"], index=1)
htf_interval = st.sidebar.selectbox("CRT HTF Range Source", ["1h", "1d", "1wk"], index=1)

# Set dynamic lookup parameters to avoid API request limits
ltf_period_map = {"1m": "1d", "5m": "5d", "15m": "5d", "1h": "1mo"}
htf_period_map = {"1h": "1mo", "1d": "3mo", "1wk": "1y"}

# Capital setup in Rands (R)
st.sidebar.write("---")
capital_zar = st.sidebar.number_input("Account Capital (R)", value=10000.0, step=500.0)
risk_percent = st.sidebar.slider("Risk per Trade (%)", 0.5, 5.0, 1.0)

# --- Cloud Data Fetch Engine ---
@st.cache_data(ttl=15) # Keep data fresh and update cache every 15 seconds
def fetch_cloud_market_data(symbol, period, interval):
    try:
        df = yf.download(tickers=symbol, period=period, interval=interval, progress=False)
        if df.empty:
            return None
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        return df.dropna()
    except Exception:
        return None

# Execution
with st.spinner("Streaming data from global market cloud..."):
    df_ltf = fetch_cloud_market_data(ticker_symbol, ltf_period_map[ltf_interval], ltf_interval)
    df_htf = fetch_cloud_market_data(ticker_symbol, htf_period_map[htf_interval], htf_interval)

decimals = 5 if ("=X" in ticker_symbol and "JPY" not in ticker_symbol) else 2

# --- Execution & Logic core ---
if df_ltf is not None and df_htf is not None and len(df_ltf) >= 3 and len(df_htf) >= 2:
    
    # 1. Establish the HTF CRT Range (Using the previous completed candle)
    crt_candle = df_htf.iloc[-2]
    crt_high = float(crt_candle['High'])
    crt_low = float(crt_candle['Low'])
    equilibrium = (crt_high + crt_low) / 2.0
    
    # 2. Get Live Executable Price
    current_price = float(df_ltf['Close'].iloc[-1])
    
    # 3. Process Signals
    recent_high = float(df_ltf['High'].iloc[-1])
    recent_low = float(df_ltf['Low'].iloc[-1])
    recent_close = float(df_ltf['Close'].iloc[-1])
    
    # Sweep Check
    swept_high = recent_high > crt_high and recent_close < crt_high
    swept_low = recent_low < crt_low and recent_close > crt_low
    
    # Imbalance Check (Simple Fair Value Gap Detection)
    c1_low = float(df_ltf['Low'].iloc[-3])
    c3_high = float(df_ltf['High'].iloc[-1])
    fvg_exists = c1_low > c3_high
    
    if swept_high:
        signal = "BEARISH"
        confidence = 88.0 if fvg_exists else 65.0
        entry_price = current_price
        stop_loss = recent_high + (recent_high * 0.0005)
        take_profit = crt_low
        reasoning = (
            f"Liquidity Sweep confirmed. Price aggressively ran buy stops above the HTF Range High ({crt_high:.{decimals}f}) "
            f"leaving a strong wick rejection. Expecting order flow to target the Range Low."
        )
    elif swept_low:
        signal = "BULLISH"
        confidence = 92.0 if fvg_exists else 70.0
        entry_price = current_price
        stop_loss = recent_low - (recent_low * 0.0005)
        take_profit = crt_high
        reasoning = (
            f"Liquidity Sweep confirmed. Price swept sell stops below the HTF Range Low ({crt_low:.{decimals}f}) "
            f"and rejected cleanly. Targets are set on premium external liquidity structures."
        )
    else:
        signal = "NEUTRAL"
        confidence = 0.0
        entry_price = current_price
        stop_loss = 0.0
        take_profit = 0.0
        
        # Determine internal market zone
        if current_price > equilibrium:
            reasoning = f"Market is currently trading inside a PREMIUM Zone (Above {equilibrium:.{decimals}f}). Waiting on a sweep confirmation."
        else:
            reasoning = f"Market is currently trading inside a DISCOUNT Zone (Below {equilibrium:.{decimals}f}). Waiting on a sweep confirmation."

    # --- UI Rendering ---
    st.subheader("📡 Live Analytics Feed")
    
    if signal == "BULLISH":
        st.success(f"🟢 SIGNAL: BULLISH | Confidence: {confidence}%")
    elif signal == "BEARISH":
        st.error(f"🔴 SIGNAL: BEARISH | Confidence: {confidence}%")
    else:
        st.warning(f"⚪ SIGNAL: NO ACTIVE CRITERIA | Confidence: --")

    col_stat1, col_stat2, col_stat3 = st.columns(3)
    col_stat1.metric(label="Live Close Price", value=f"{current_price:,.{decimals}f}")
    col_stat2.metric(label="HTF Range High", value=f"{crt_high:,.{decimals}f}")
    col_stat3.metric(label="HTF Range Low", value=f"{crt_low:,.{decimals}f}")

    st.write("---")

    # Clean logic breakdown panel
    st.markdown("### 📋 System Logic Breakdown")
    st.info(reasoning)

    # Risk Calculation Panel (ZAR Output)
    st.markdown("### 🎯 Target Execution Protection Matrix")
    
    if signal != "NEUTRAL" and stop_loss > 0:
        risk_distance = abs(entry_price - stop_loss)
        risk_capital_zar = capital_zar * (risk_percent / 100)
        
        st.write(f"**Target Entry Price:** {entry_price:.{decimals}f}")
        st.write(f"**Calculated Stop Loss:** {stop_loss:.{decimals}f}")
        st.write(f"**Calculated Take Profit:** {take_profit:.{decimals}f}")
        
        st.write("---")
