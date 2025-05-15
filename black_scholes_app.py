import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm

# ----------- Black-Scholes Pricing ------------
class BlackScholes:
    def __init__(self, S, K, r, t, sigma):
        self.S = S
        self.K = K
        self.r = r
        self.t = t
        self.sigma = sigma

    def d1(self):
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.t) / (self.sigma * np.sqrt(self.t))

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.t)

    def call_price(self):
        d1, d2 = self.d1(), self.d2()
        return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.t) * norm.cdf(d2)

    def put_price(self):
        d1, d2 = self.d1(), self.d2()
        return self.K * np.exp(-self.r * self.t) * norm.cdf(-d2) - self.S * norm.cdf(-d1)

# ----------- Streamlit UI ------------
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

# ----------- Heatmap Inputs ------------
st.subheader("P&L Heatmap")

grid_size = 10
col6, col7 = st.columns(2)
with col6:
    S_min = st.slider("Min Spot Price for Heatmap", min_value=1.0, max_value=S, value=float(S * 0.8))
    S_max = st.slider("Max Spot Price for Heatmap", min_value=S, max_value=S * 2, value=float(S * 1.2))
with col7:
    sigma_min = st.slider("Min Volatility (σ) for Heatmap", min_value=0.01, max_value=sigma, value=float(sigma * 0.5))
    sigma_max = st.slider("Max Volatility (σ) for Heatmap", min_value=sigma, max_value=sigma * 1.5, value=float(sigma * 1.2))

spot_range = np.linspace(S_min, S_max, grid_size)
vol_range = np.linspace(sigma_min, sigma_max, grid_size)

# Compute PNL Matrices
def compute_pnl(option_type):
    matrix = np.zeros((grid_size, grid_size))
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs = BlackScholes(spot, K, r, t, vol)
            if option_type == 'call':
                pnl = bs.call_price() - max(spot - K, 0)
            elif option_type == 'put':  
                pnl = bs.put_price() - max(K - spot, 0)
            matrix[i, j] = pnl
    return matrix

call_pnl = compute_pnl('call')
put_pnl = compute_pnl('put')

# Plot heatmaps
def plot_heatmap(data, title):
    df = pd.DataFrame(data, index=np.round(vol_range, 2), columns=np.round(spot_range, 2))
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df, annot=True, fmt=".2f", cmap="RdYlGn", cbar_kws={'label': 'P&L'}, ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Spot Price")
    ax.set_ylabel("Volatility")
    return fig

# Layout for side-by-side heatmaps
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("📈Call P&L")
    fig1 = plot_heatmap(call_pnl, "Call P&L")
    st.pyplot(fig1)

with col_right:
    st.subheader("📉Put P&L")
    fig2 = plot_heatmap(put_pnl, "Put P&L")
    st.pyplot(fig2)
