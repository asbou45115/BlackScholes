import streamlit as st
from BlackScholes import BlackScholes

# ----------- Streamlit UI ------------
def create_ui():
    st.set_page_config(
        page_title='Black-Scholes model',
        layout='wide'
        )

    st.title("Black-Scholes Options Pricing")

    # Input Fields for Single Calculation
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        S = st.number_input("Spot Price", value=120.0)
    with col2:
        K = st.number_input("Strike Price", value=130.0)
    with col3:
        t = st.number_input("Time to Maturity (Years)", value=1.0)
    with col4:
        sigma = st.number_input("Volatility (σ)", value=0.2)
    with col5:
        r = st.number_input("Risk-Free Interest Rate", value=0.05)

    # Calculate Black-Scholes prices
    bs = BlackScholes(S, K, r, t, sigma)
    call_val = bs.call_price()
    put_val = bs.put_price()

    # Display Results
    col_call, col_put = st.columns(2)
    with col_call:
        st.markdown(
            f"<div style='background-color:#b5f7b4;padding:10px;border-radius:10px;text-align:center;'>"
            f"<h3 style = 'color:black'>CALL Value</h3><h1 style='color:black;'>${call_val:.2f}</h1></div>",
            unsafe_allow_html=True
        )
    with col_put:
        st.markdown(
            f"<div style='background-color:#f7c4c4;padding:10px;border-radius:10px;text-align:center;'>"
            f"<h3 style = 'color:black'>PUT Value</h3><h1 style='color:black;'>${put_val:.2f}</h1></div>",
            unsafe_allow_html=True
        )

    return S, K, t, sigma, r