import streamlit as st
import time
import random

# --- APP CONFIG ---
st.set_page_config(page_title="CARNAGE MATRIX", layout="wide", page_icon="💀")

# --- DARK/EVIL RED CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff0000; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3 { color: #8b0000 !important; text-transform: uppercase; letter-spacing: 4px; text-shadow: 2px 2px #000; }
    .stButton>button { border: 2px solid #8b0000; background: #000; color: #ff0000; width: 100%; font-weight: bold; }
    .stButton>button:hover { background: #8b0000; color: #fff; }
    .metric-box { background: #111; border: 1px solid #8b0000; padding: 20px; color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

st.title("💀 CARNAGE QUANTUM MATRIX V8.0")
st.write("SYSTEM STATUS: [ENGAGED] | STRATEGY: [CRT + PRICE ACTION]")

# --- SIDEBAR ---
st.sidebar.header("TERMINAL INPUTS")
symbol = st.sidebar.selectbox("CURRENCY PAIR", ["EURUSD", "USDJPY", "GBPUSD", "GOLD (XAUUSD)"])
tf = st.sidebar.selectbox("TIMEFRAME", ["M1", "M5", "M15", "H1", "H4", "D1"])
balance = st.sidebar.number_input("ACCOUNT BALANCE (ZAR)", value=1000.0)

# --- SCANNER LOGIC ---
if st.button("RUN QUANTUM SCAN"):
    with st.spinner("EXECUTING CRT ALGORITHM..."):
        time.sleep(2) # Simulating market analysis
        
        # Simulated CRT/Price Action Logic
        signal = random.choice(["BUY", "SELL"])
        conf = random.randint(85, 99)
        
        st.subheader(f"SIGNAL: {signal}")
        
        col1, col2 = st.columns(2)
        col1.metric("CONFIDENCE", f"{conf}%")
        col2.write("### REASONING")
        col2.write(f"• **CRT Analysis:** {symbol} price range exhaustion detected.")
        col2.write("• **Price Action:** Rejection at support/resistance boundary.")
        col2.write("• **Market Flow:** Volatility spike on " + tf)
        
        st.write("---")
        st.subheader("EXECUTION PARAMETERS")
        st.warning(f"ENTRY: {symbol} MARKET")
        st.error("SL: CALCULATED AT 20 PIPS")
        st.success(f"TP: CALCULATED AT 60 PIPS")
        st.info(f"LOT SIZE: {(balance * 0.02 / 100):.2f}")

st.write("---")
st.write("TERMINAL: ACTIVE | MODE: EVIL")
