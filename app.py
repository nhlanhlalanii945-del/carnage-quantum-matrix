import streamlit as st
import random
import time

# --- APP CONFIG ---
st.set_page_config(page_title="Carnage Quantum Matrix", page_icon="⚡", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0c10; color: #c5c6c7; }
    .stButton>button { width: 100%; background-color: #66fcf1; color: #000; font-weight: bold; }
    h1, h2, h3 { color: #66fcf1 !important; }
    .css-1544g2n { color: #66fcf1; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("⚡ TERMINAL CONTROLS")
symbol = st.sidebar.selectbox("Select Asset", ["EURUSD", "GOLD (XAUUSD)", "USDZAR", "BTCUSD"])
risk_amount = st.sidebar.number_input("Risk Amount (ZAR)", value=200.0)
leverage = st.sidebar.slider("Leverage", 1, 100, 30)

# --- MAIN INTERFACE ---
st.title("⚡ CARNAGE QUANTUM MATRIX V5.2")
st.write("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Market Signal Engine")
    if st.button("RUN QUANTUM SCAN"):
        with st.spinner("Analyzing Market Depth..."):
            time.sleep(1.5) # Simulating analysis time
            
            # Logic Placeholder
            signal_type = random.choice(["BUY", "SELL"])
            confidence = random.randint(75, 99)
            
            st.success(f"Signal Found: {signal_type}")
            st.metric("Confidence Level", f"{confidence}%")
            st.write(f"Trend Analysis: Bullish momentum detected on {symbol}.")

with col2:
    st.subheader("Risk Management")
    st.write(f"**Asset:** {symbol}")
    st.write(f"**Exposure:** R{risk_amount}")
    
    # Simple calculation
    stop_loss_dist = 0.002 # Simplified points
    lot_size = risk_amount / (stop_loss_dist * 10000)
    
    st.info(f"Recommended Lot: {lot_size:.2f}")
    st.warning("Ensure proper margin before execution.")

st.write("---")
st.footer = "SYSTEM STATUS: ONLINE | QUANTUM MATRIX v5.2"
st.write(st.footer)
