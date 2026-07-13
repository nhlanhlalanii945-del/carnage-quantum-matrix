import streamlit as st

st.set_page_config(page_title="Carnage Quantum Matrix", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0c10; color: #c5c6c7; }
    h1 { color: #66fcf1 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ CARNAGE QUANTUM MATRIX V1.0")
st.write("---")

risk_zar = st.number_input("Risk Amount (ZAR)", value=200.0)
st.write(f"Risk set to: R{risk_zar}")
