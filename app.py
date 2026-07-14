import streamlit as st
import yfinance as yf
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="CARNAGE QUANTUM MATRIX V12.0", layout="wide", page_icon="💀")

# --- CUSTOM CSS (EVIL TERMINAL AESTHETIC) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff0000; font-family: 'Courier New', Courier, monospace; }
    h1 { color: #8b0000 !important; text-transform: uppercase; letter-spacing: 4px; border-bottom: 2px solid #8b0000; padding-bottom: 10px; }
    h2 { color: #8b0000 !important; text-transform: uppercase; letter-spacing: 2px; }
    .stButton>button { border: 2px solid #8b0000; background: #000; color: #ff0000; width: 100%; height: 60px; font-weight: bold; font-size: 20px; text-transform: uppercase; }
    .stButton>button:hover { background: #8b0000; color: #fff; }
    .metric-card { background: #111; border: 2px solid #8b0000; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
    .signal-box { background: #0a0000; border: 2px solid #8b0000; padding: 20px; color: #ff0000; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("💀 CARNAGE QUANTUM MATRIX V12.0")
st.write("STATUS: [ONLINE] | DATA FEED: [LIVE MARKET]")

# --- MAIN INPUT SECTION ---
st.subheader("TERMINAL INPUTS")
col1, col2, col3 = st.columns(3)

# Asset Dictionary
assets = {"EURUSD": "EURUSD=X", "USDJPY": "JPY=X", "GBPUSD": "GBPUSD=X", "GOLD": "GC=F"}

with col1:
    pair = st.selectbox("SELECT ASSET", list(assets.keys()))
with col2:
    tf = st.selectbox("TIMEFRAME", ["1h", "1d", "1wk"])
with col3:
    balance = st.number_input("ACCOUNT BALANCE (ZAR)", value=200.0, step=10.0)

# --- EXECUTION ---
if st.button("RUN QUANTUM SCAN"):
    try:
        with st.spinner("CALCULATING MARKET FLOW..."):
            # Fetch Live Data
            ticker = yf.Ticker(assets[pair])
            data = ticker.history(period="10d", interval=tf)
            
            if data.empty:
                st.error("DATA FETCH FAILED. TRY DIFFERENT TIMEFRAME.")
            else:
                current_price = data['Close'].iloc[-1]
                prev_price = data['Close'].iloc[-2]
                
                # Logic Engine
                change = ((current_price - prev_price) / prev_price) * 100
                confidence = np.clip(abs(change) * 15 + 70, 70, 99)
                signal = "BUY" if change > 0 else "SELL"
                
                # Financial Math
                risk_amount = balance * 0.05  # 5% Risk
                lot_size = risk_amount / 100
                sl = current_price * 0.998 if signal == "BUY" else current_price * 1.002
                tp = current_price * 1.005 if signal == "BUY" else current_price * 0.995

                # DISPLAY RESULTS
                st.write("---")
                
                # Signal Output
                st.markdown(f'<div class="signal-box"><h2>SIGNAL FOUND: {signal}</h2></div>', unsafe_allow_html=True)
                
                # Metrics
                m1, m2 = st.columns(2)
                m1.metric("CONFIDENCE LEVEL", f"{confidence:.1f}%")
                m2.metric("CURRENT PRICE", f"{current_price:.4f}")
                
                # Risk Management
                st.subheader("RISK MANAGEMENT")
                st.write(f"**ASSET:** {pair}")
                st.write(f"**EXPOSURE:** R{balance:.2f}")
                
                # Execution
                st.info(f"ENTRY: {current_price:.4f}")
                col_sl, col_tp = st.columns(2)
                col_sl.warning(f"STOP LOSS: {sl:.4f}")
                col_tp.success(f"TAKE PROFIT: {tp:.4f}")
                
                st.write(f"**RECOMMENDED LOT:** {lot_size:.2f}")
                st.caption("Ensure proper margin before execution.")

    except Exception as e:
        st.error(f"CRITICAL ERROR: {e}")

# --- FOOTER ---
st.write("---")
st.caption("SYSTEM STATUS: LIVE | PROVIDER: YFINANCE")
