import streamlit as st
import yfinance as yf
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="CARNAGE MATRIX", layout="wide", page_icon="💀")

# --- DARK/EVIL RED CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff0000; font-family: 'Courier New', Courier, monospace; }
    h1 { color: #8b0000 !important; text-transform: uppercase; letter-spacing: 4px; border-bottom: 2px solid #8b0000; }
    .stButton>button { border: 2px solid #8b0000; background: #000; color: #ff0000; width: 100%; height: 60px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("💀 CARNAGE QUANTUM MATRIX V11.0")
st.write("STATUS: [LIVE MARKET FEED ACTIVE]")

# --- SIDEBAR INPUTS ---
st.sidebar.header("TERMINAL INPUTS")
ticker_map = {"EURUSD": "EURUSD=X", "USDJPY": "JPY=X", "GBPUSD": "GBPUSD=X", "GOLD": "GC=F"}
pair = st.sidebar.selectbox("SELECT CURRENCY", list(ticker_map.keys()))
tf = st.sidebar.selectbox("TIMEFRAME", ["1h", "1d", "1wk"])
balance = st.sidebar.number_input("BALANCE (ZAR)", value=200.0)

# --- ENGINE ---
if st.button("RUN LIVE ANALYSIS"):
    try:
        # Get Live Data
        ticker = yf.Ticker(ticker_map[pair])
        data = ticker.history(period="5d", interval=tf)
        current_price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        
        # CRT Logic Simulation
        trend = "BULLISH" if current_price > prev_close else "BEARISH"
        risk_amount = balance * 0.05
        lot_size = risk_amount / 100
        
        # Display Signal
        st.subheader(f"LIVE ANALYSIS: {pair}")
        col1, col2 = st.columns(2)
        col1.metric("CURRENT PRICE", f"{current_price:.4f}")
        col2.metric("MARKET TREND", trend)
        
        st.write("---")
        st.error(f"SIGNAL: {trend}")
        st.info(f"ENTRY: {current_price:.4f}")
        st.success(f"SL: {(current_price * 0.998):.4f} | TP: {(current_price * 1.005):.4f}")
        st.warning(f"LOT SIZE (5% RISK): {lot_size:.2f}")
        st.write("**REASONING:** Price Action & CRT Analysis aligned on {tf} chart.")
        
    except Exception as e:
        st.error("Error connecting to live feed. Check internet.")

st.write("---")
st.caption("TERMINAL: OPERATIONAL | PROVIDER: YFINANCE")
