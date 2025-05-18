import streamlit as st
from st_ui import create_ui
from heatmap import render_heatmap

S, K, t, sigma, r = create_ui()
render_heatmap(S, K, sigma, r)

with st.expander("Interpretation Help"):
    st.write("""
    ### How to read this heatmap:
    
    - Each cell shows the P&L for the option at a specific spot price (current value of asset) and date.
    - The initial option price is calculated based on the parameters you set above using a Black Scholes model.
    - For dates before expiration, the P&L is calculated as the difference between the option's price on that date and the initial price.
    - At expiration, the P&L is calculated as the difference between the option's intrinsic value and the initial price.
    - Red cells indicate losses, green cells indicate profits.
    
    ### DISCLAIMER: 
    
    This model is for educational purposes only and should not be used as financial advice
    """)