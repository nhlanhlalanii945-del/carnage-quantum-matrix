import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# ----------------------------------------------------
# PAGE CONFIG & STYLING
# ----------------------------------------------------
st.set_page_config(
    page_title="CRT Cloud Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Mode CSS Tweaks
st.markdown("""
    <style>
    .stMetric {
        background-color: #1e1e1e;
        border: 1px solid #333333;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_render_html=True)

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.title("⚡ CRT Cloud Market Terminal")
st.caption("No Windows PC. No local MT5 terminal. 100% cloud-native live data via Yahoo Finance.")
st.write("---")

# ----------------------------------------------------
# SIDEBAR SETTINGS
# ----------------------------------------------------
st.sidebar.header("⚙️ Configuration")

# Dynamic asset map (Forex and Gold Spot proxy)
asset_map = {
    "Gold Spot (Proxy: GC=F)": "GC=F",
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "GBP/JPY": "GBPJPY=X"
}

selected_asset = st.sidebar.selectbox("Select Trading Asset", list(asset_map.keys()), index=0)
ticker = asset_map[selected_asset]

# Interval setup
ltf_interval = st.sidebar.selectbox(
    "Execution TF (Lower Timeframe Chart)",
    ["1m", "5m", "15m", "30m", "1h"],
    index=1
)

htf_interval = st.sidebar.selectbox(
    "CRT Range TF (Higher Timeframe Source)",
    ["1h", "1d", "1wk"],
    index=1
)

# Dynamic periods to prevent API errors
ltf_period_map = {"1m": "1d", "5m": "5d", "15m": "5d", "30m": "5d", "1h": "1mo"}
htf_period_map = {"1h": "1mo", "1d": "3mo", "1wk": "1y"}

ltf_period = ltf_period_map[ltf_interval]
htf_period = htf_period_map[htf_interval]

# ----------------------------------------------------
# DATA LOADER
# ----------------------------------------------------
@st.cache_data(ttl=10) # Auto-refresh data cache every 10 seconds
def fetch_market_data(symbol, period, interval):
    try:
        df = yf.download(tickers=symbol, period=period, interval=interval, progress=False)
        if df.empty:
            return None
        # Standardize multi-index columns if yfinance returns them
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        return df.dropna()
    except Exception:
        return None

# Fetch Data
with st.spinner("Syncing live market feeds..."):
    df_ltf = fetch_market_data(ticker, ltf_period, ltf_interval)
    df_htf = fetch_market_data(ticker, htf_period, htf_interval)

# Determine decimal formatting based on pair type
decimals = 5 if ("=X" in ticker and "JPY" not in ticker) else 2

if df_ltf is not None and df_htf is not None and len(df_ltf) >= 2 and len(df_htf) >= 2:
    
    # ----------------------------------------------------
    # CRT RANGE CALCULATION (Using previous closed HTF candle)
    # ----------------------------------------------------
    crt_candle = df_htf.iloc[-2]  # The completed previous HTF candle
    crt_high = float(crt_candle['High'])
    crt_low = float(crt_candle['Low'])
    equilibrium = (crt_high + crt_low) / 2.0
    
    # Quarterly ranges (25% and 75% levels)
    premium_quarter = crt_low + 0.75 * (crt_high - crt_low)
    discount_quarter = crt_low + 0.25 * (crt_high - crt_low)
    
    # Current Execution Price
    current_price = float(df_ltf['Close'].iloc[-1])
    price_change = current_price - float(df_ltf['Close'].iloc[-2])
    pct_change = (price_change / float(df_ltf['Close'].iloc[-2])) * 100

    # ----------------------------------------------------
    # METRICS DISPLAY
    # ----------------------------------------------------
    st.subheader(f"📊 Live {selected_asset} Overview")
    
    col_price, col_high, col_eq, col_low = st.columns(4)
    col_price.metric(
        label="Live Price",
        value=f"{current_price:.{decimals}f}",
        delta=f"{price_change:+.{decimals}f} ({pct_change:+.2f}%)"
    )
    col_high.metric(label=f"HTF Range High ({htf_interval})", value=f"{crt_high:.{decimals}f}")
    col_eq.metric(label="Equilibrium (50%)", value=f"{equilibrium:.{decimals}f}")
    col_low.metric(label=f"HTF Range Low ({htf_interval})", value=f"{crt_low:.{decimals}f}")

    # ----------------------------------------------------
    # CRT STATE ANALYSIS
    # ----------------------------------------------------
    st.write("### 🎯 Candle Range Theory (CRT) Analysis")
    
    if current_price > crt_high:
        st.error(f"🚨 Price has swept above the HTF Range High ({crt_high:.{decimals}f}). Watch out for external liquidity sweeps & reversals!")
    elif current_price < crt_low:
        st.success(f"🚨 Price has swept below the HTF Range Low ({crt_low:.{decimals}f}). Look for liquidity sweeps & LTF structural shifts!")
    elif current_price > equilibrium:
        st.info(f"🔴 Price is trading in the **PREMIUM** zone (Above 50% Equilibrium). Look for shorts if LTF trend shifts bearish.")
    else:
        st.success(f"🟢 Price is trading in the **DISCOUNT** zone (Below 50% Equilibrium). Look for longs if LTF trend shifts bullish.")

    # ----------------------------------------------------
    # INTERACTIVE PLOTLY CHART
    # ----------------------------------------------------
    st.write("### 📈 Live Price Action Chart")
    
    fig = go.Figure(data=[go.Candlestick(
        x=df_ltf.index,
        open=df_ltf['Open'],
        high=df_ltf['High'],
        low=df_ltf['Low'],
        close=df_ltf['Close'],
        name="Price Action"
    )])
    
    # Overlay HTF Ranges
    fig.add_hline(y=crt_high, line_dash="solid", line_color="red", 
                  annotation_text=f"HTF High ({crt_high:.{decimals}f})", annotation_position="top left")
    fig.add_hline(y=equilibrium, line_dash="dash", line_color="orange", 
                  annotation_text=f"Equilibrium ({equilibrium:.{decimals}f})", annotation_position="right")
    fig.add_hline(y=crt_low, line_dash="solid", line_color="green", 
                  annotation_text=f"HTF Low ({crt_low:.{decimals}f})", annotation_position="bottom left")
    
    # Optional quarterly guidelines
    fig.add_hline(y=premium_quarter, line_dash="dot", line_color="#ff4d4d", opacity=0.3)
    fig.add_hline(y=discount_quarter, line_dash="dot", line_color="#4dff4d", opacity=0.3)

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=550,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------------------
    # RAW DATA FEED FOR AUDITING
    # ----------------------------------------------------
    with st.expander("📁 Raw Live Feed Data"):
        st.dataframe(df_ltf.tail(15))

else:
    st.error("⚠️ Data Sync Interrupted. The markets might be closed (weekends), or Yahoo Finance is experiencing high traffic. Try refreshing or switching timeframes.")
