import streamlit as st
from st_ui import create_ui
from heatmap import render_heatmap

S, K, t, sigma, r = create_ui()
render_heatmap(S, K, t, sigma, r)

with st.expander("Interpretation Help + Info"):
    st.write("""
    ### How to read this heatmap:
    
    - Each cell shows the P&L for the option at a specific spot price (current value of asset) and date.
    - The initial option price is calculated based on the parameters you set above using a Black Scholes model.
    - For dates before expiration, the P&L is calculated as the difference between the option's price on that date and the initial price.
    - At expiration, the P&L is calculated as the difference between the option's intrinsic value and the initial price.
    - The greener the square, the more profit and the redder the square the less profit (and potential loss).
    
    **DISCLAIMER: The profit calculation for times prior to the actual expiry is very simple in this model and requires more advanced modelling**
    """)
    
    st.write(
        """
        This model is used to estimate the theoretical value of options (calls and puts).
        The formula for the price of a **call option** and **put option** respectively is:
        """
    )
    st.latex(r"C = N(d_1)S_t - N(d_2)Ke^{-rt}")
    st.latex(r"P = N(-d_2)Ke^{-rt} - N(d_1)S_t")
    st.write(
        """
        Where:
        
        - \( C \) = Call option price  
        - \( P \) = Put option price
        - \( S_t \) = Current price of the underlying asset  
        - \( K \) = Strike price  
        - \( r \) = Risk-free interest rate  
        - \( t \) = Time to maturity (in years)  
        - \( N(d_i) \) = Cumulative distribution function of the standard normal distribution  
        - \( d_1 \) and \( d_2 \) are defined as:
        """
    )
    st.latex(r"d_1 = \frac{\ln(S_t/K) + (r + \frac{\sigma^2}{2})t}{\sigma \sqrt{t}}")
    st.latex(r"d_2 = d_1 - \sigma \sqrt{t}")
    
    st.write(
        """
        - The max risk is the initial cost of the option itself. This occurs when the option 'expires worthless' where either an asset 
        closes below call's strike price at expiry (for a call option) or closes above put's strike price at expiry (for put option).
        
        - For a put, profit increases linearly as the stock approaches 0 while for a call, profit increases linearly as stock increases 
        and so theoretically there is no profit cap
        """
    )
    
st.info("DISCLAIMER: This model is for educational purposes only and should not be used as financial advice")