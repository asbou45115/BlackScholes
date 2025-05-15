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
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🧮 Black-Scholes Pricing Model</h1>", unsafe_allow_html=True)

# Input columns
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    S = st.number_input("Current Asset Price", value=120.0, format="%.4f")
with col2:
    K = st.number_input("Strike Price", value=130.0, format="%.4f")
with col3:
    t = st.number_input("Time to Maturity (Years)", value=1.0, format="%.4f")
with col4:
    sigma = st.number_input("Volatility (σ)", value=0.2, format="%.4f")
with col5:
    r = st.number_input("Risk-Free Interest Rate", value=0.05, format="%.4f")

# Compute values
bs = BlackScholes(S, K, r, t, sigma)
call_val = bs.call_price()
put_val = bs.put_price()

# Display result boxes
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        f"<div style='background-color:#b5f7b4;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>CALL Value</h3><h1 style='color:green;'>${call_val:.2f}</h1></div>",
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        f"<div style='background-color:#f7c4c4;padding:20px;border-radius:10px;text-align:center;'>"
        f"<h3>PUT Value</h3><h1 style='color:red;'>${put_val:.2f}</h1></div>",
        unsafe_allow_html=True
    )

# ---------- PNL Heatmap ----------
st.subheader("📊 PNL Heatmap vs Volatility and Asset Price")

contracts = st.number_input("Number of Contracts", value=1, step=1)
position_type = st.selectbox("Position Type", ["Long Call", "Short Call", "Long Put", "Short Put"])

# Generate heatmap data
spot_range = np.linspace(S * 0.5, S * 1.5, 50)
vol_range = np.linspace(0.01, 1.0, 50)

pnl_matrix = np.zeros((len(vol_range), len(spot_range)))

for i, vol in enumerate(vol_range):
    for j, spot in enumerate(spot_range):
        bs = BlackScholes(spot, K, r, t, vol)
        if position_type == "Long Call":
            pnl = (spot - K) * contracts - bs.call_price() * contracts
        elif position_type == "Short Call":
            pnl = bs.call_price() * contracts - (spot - K) * contracts
        elif position_type == "Long Put":
            pnl = (K - spot) * contracts - bs.put_price() * contracts
        else:  # Short Put
            pnl = bs.put_price() * contracts - (K - spot) * contracts
        pnl_matrix[i, j] = pnl

# Convert to DataFrame for Seaborn
df = pd.DataFrame(pnl_matrix, index=np.round(vol_range, 2), columns=np.round(spot_range, 2))

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df, cmap="coolwarm", cbar_kws={'label': 'PNL'}, ax=ax)
ax.set_xlabel("Spot Price")
ax.set_ylabel("Volatility (σ)")
st.pyplot(fig)
