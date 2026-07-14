import streamlit as st

st.title("Carnage Quantum Matrix")
st.write("System Status: Active")

risk = st.number_input("Enter Risk Amount (ZAR)", value=200.0)
if st.button("Calculate"):
    st.write(f"Risk confirmed at R{risk}")
