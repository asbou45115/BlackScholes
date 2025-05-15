import streamlit as st
import numpy as np
from scipy.stats import norm

class BlackScholes:
    def __init__(self, spot_price, strike_price, interest_rate, time_to_maturity, volatility):
        self.S_t = spot_price
        self.K = strike_price
        self.r = interest_rate
        self.t = time_to_maturity
        self.sigma = volatility
        
    def calculate(self):
        S_t = self.S_t
        K = self.K
        r = self.r
        t = self.t
        sigma = self.sigma
        
        d1 = (np.log(S_t / K) + (r + (sigma ** 2 / 2)) * t) / (sigma * np.sqrt(t))
        d2 = d1 - sigma * np.sqrt(t)
        
        call_price = norm.cdf(d1) * S_t - norm.cdf(d2) * K * np.exp(-r * t)
        put_price = norm.cdf(-d2) * K * np.exp(-r * t) - norm.cdf(-d1) * S_t
        
        return call_price, put_price
            
st.title("📈 Black-Scholes Option Pricing")

st.sidebar.header("Input Parameters")

spot_price = st.sidebar.slider("Spot Price (S_t)", min_value=0.0, max_value=100.0, value=31.55, step=0.1)
strike_price = st.sidebar.slider("Strike Price (K)", min_value=0.0, max_value=100.0, value=22.75, step=0.1)
interest_rate = st.sidebar.slider("Interest Rate (r)", min_value=0.0, max_value=0.2, value=0.05, step=0.005)
time_to_maturity = st.sidebar.slider("Time to Maturity (t, in years)", min_value=0.1, max_value=10.0, value=3.5, step=0.1)
volatility = st.sidebar.slider("Volatility (σ)", min_value=0.01, max_value=2.0, value=0.5, step=0.01)

# Calculate price
bs_model = BlackScholes(spot_price, strike_price, interest_rate, time_to_maturity, volatility)
call_price, put_price = bs_model.calculate()

st.subheader("🧮 Call Option Price")
st.success(f"The Black-Scholes Call Option Price is: **${call_price:.2f}**")