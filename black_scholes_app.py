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
            
if __name__ == "__main__":
    BS = BlackScholes(31.55, 22.75, 0.05, 3.5, 0.5)
    BS.calculate()