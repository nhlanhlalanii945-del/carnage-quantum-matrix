import streamlit as st
import yfinance as yf
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="CARNAGE TRADING TERMINAL", layout="wide", page_icon="💀")

# --- EVIL DARK CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff0000; font-family: 'Courier New', Courier, monospace; }
    h1 { color: #8b0000 !important; text-transform: uppercase; letter-spacing: 4px; border-bottom: 2px solid #8b0000; padding-bottom: 10px; }
    .stButton>button { border: 2px solid #8b0000; background: #000; color: #ff0000; width: 100%; height: 60px; font-weight: bold; }
    .metric-box { background: #111; border: 2px solid #8b0000; padding: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("💀 CARNAGE TRADING TERMINAL V5.2")
st.write("STATUS: [LIVE MARKET FEED ACTIVE]")

# --- INPUTS ---
col1, col2, col3 = st.columns(3)
assets = {"EURUSD": "EURUSD=X", "USDJPY": "JPY=X", "GBPUSD": "GBPUSD=X", "GOLD": "GC=F"}
timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1wk', '1mo']

pair = col1.selectbox("SELECT ASSET", list(assets.keys()))
tf = col2.selectbox("TIMEFRAME", timeframes)
balance = col3.number_input("ACCOUNT BALANCE (ZAR)", value=200.0)

if st.button("RUN LIVE ANALYSIS"):
    try:
        # LIVE DATA ENGINE
        ticker = yf.Ticker(assets[pair])
        df = ticker.history(period="1mo", interval=tf)
        
        if not df.empty:
            current_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2]
            
            # SIGNAL LOGIC
            trend = "BULLISH" if current_price > prev_price else "BEARISH"
            risk = balance * 0.05
            lot = risk / 100
            
            # DISPLAY
            st.write("---")
            st.subheader(f"SIGNAL: {trend}")
            
            c1, c2 = st.columns(2)
            c1.metric("LIVE PRICE", f"{current_price:.5f}")
            c2.metric("CHANGE", f"{((current_price-prev_price)/prev_price)*100:.2f}%")
            
            st.write("### ANALYSIS BREAKDOWN")
            st.info(f"Market movement detected on {tf} timeframe.")
            st.warning(f"ENTRY: {current_price:.5f} | SL: {(current_price*0.999):.5f} | TP: {(current_price*1.002):.5f}")
            st.success(f"SUGGESTED LOT SIZE: {lot:.2f}")
        else:
            st.error("LIVE FEED ERROR: RETRY")
    except Exception as e:
        st.error(f"SYSTEM ERROR: {e}")
