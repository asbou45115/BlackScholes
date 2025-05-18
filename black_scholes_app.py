import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
from datetime import datetime, timedelta
import matplotlib.colors as mcolors

# ----------- Black-Scholes Pricing ------------
class BlackScholes:
    '''
    S: spot price,
    K: strike price,
    r: risk-free interest rate,
    t: time to maturity,
    sigma: volatility
    '''
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
        if self.t <= 0:
            return max(0, self.S - self.K)
        d1, d2 = self.d1(), self.d2()
        return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.t) * norm.cdf(d2)

    def put_price(self):
        if self.t <= 0:
            return max(0, self.K - self.S)
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

# ----------- New Date-Strike P&L Heatmap ------------
st.subheader("P&L Heatmap by Strike and Date")

# Set date range
today = datetime.now().date()
col_date1, col_date2 = st.columns(2)
with col_date1:
    start_date = st.date_input("Start Date", today)
with col_date2:
    expiration_date = st.date_input("Expiration Date", today + timedelta(days=30))

# Set strike price range
grid_size = 15  # Number of steps in the grid
col_strike1, col_strike2 = st.columns(2)
with col_strike1:
    min_strike = st.number_input("Min Strike Price", value=round(S * 0.8, 2), step=1.0)
with col_strike2:
    max_strike = st.number_input("Max Strike Price", value=round(S * 1.2, 2), step=1.0)

# Calculation parameters
option_type = st.radio("Option Type", ["Call", "Put"], horizontal=True)
risk_display_type = st.radio("Display", ["P&L Values", "% of Maximum Risk"], horizontal=True)
num_contracts = st.number_input("Number of Contracts (x100)", min_value=1, value=1)

# Generate date range and strike range
days_diff = (expiration_date - start_date).days
if days_diff <= 0:
    st.error("Expiration date must be after start date")
else:
    date_range = [start_date + timedelta(days=int(i * days_diff / (grid_size-1))) for i in range(grid_size)]
    date_range[-1] = expiration_date  # Ensure the last date is exactly the expiration date
    
    strike_range = np.linspace(min_strike, max_strike, grid_size)
    
    # Create P&L matrix
    matrix = np.zeros((grid_size, grid_size))
    max_risk = 0
    
    # Calculate the price of the option at the starting date
    days_to_expiry = (expiration_date - start_date).days / 365.0
    initial_bs = BlackScholes(S, K, r, days_to_expiry, sigma)
    if option_type == "Call":
        initial_price = initial_bs.call_price()
    else:  # Put
        initial_price = initial_bs.put_price()
    
    # This is the cost to enter the position
    entry_cost = initial_price * num_contracts * 100
    max_risk = entry_cost
    
    # Calculate P&L for each cell in the matrix
    for i, strike in enumerate(strike_range):
        for j, date in enumerate(date_range):
            days_to_expiry = (expiration_date - date).days / 365.0
            current_bs = BlackScholes(S, strike, r, days_to_expiry, sigma)
            
            if option_type == "Call":
                current_price = current_bs.call_price()
                if date == expiration_date:
                    pnl = (max(0, S - strike) - initial_price) * num_contracts * 100
                else:
                    # Prior to expiration, P&L is (current_price - initial_price)
                    pnl = (current_price - initial_price) * num_contracts * 100
            else:  # Put
                current_price = current_bs.put_price()
                if date == expiration_date:
                    pnl = (max(0, strike - S) - initial_price) * num_contracts * 100
                else:
                    # Prior to expiration, P&L is (current_price - initial_price)
                    pnl = (current_price - initial_price) * num_contracts * 100
            
            matrix[i, j] = pnl
    
    # Prepare matrix for display based on display type
    if risk_display_type == "% of Maximum Risk" and max_risk > 0:
        matrix = (matrix / max_risk) * 100  # Convert to percentages
        fmt = ".1f"
        cbar_label = "% of Maximum Risk"
    else:
        fmt = ".2f"
        cbar_label = "P&L ($)"
    
    # Create dataframe with rounded values for better display
    df = pd.DataFrame(matrix, index=np.round(strike_range, 2), columns=[date.strftime('%b %d') for date in date_range])
    
    # Plot heatmap
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create the heatmap
    sns.heatmap(df, annot=True, fmt=fmt, cmap="RdYlGn", center=0, cbar_kws={'label': cbar_label}, ax=ax, linewidths=0.2)
    
    title = f"{option_type} Option P&L - Strike Price vs Date"
    if risk_display_type == "% of Maximum Risk":
        title += " (% of Max Risk)"
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Strike Price", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Additional information
    with st.expander("Interpretation Help"):
        st.write("""
        ### How to read this heatmap:
        
        - Each cell shows the P&L for the option at a specific strike price and date.
        - The initial option price is calculated based on the parameters you set above.
        - For dates before expiration, the P&L is calculated as the difference between the option's price on that date and the initial price.
        - At expiration, the P&L is calculated as the difference between the option's intrinsic value and the initial price.
        - Red cells indicate losses, green cells indicate profits.
        
        ### Example:
        If you buy a call option with a strike price of $130 today, and the stock price is currently $120, this heatmap shows how your P&L would look at different future dates and if you had chosen different strike prices.
        """)