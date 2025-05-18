import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from BlackScholes import BlackScholes

def display_heatmap(matrix, risk_display_type, max_risk, option_type, spot_range, date_range, entry_cost):
    # Display adjustments
    if risk_display_type == "% of Maximum Risk" and max_risk > 0:
        matrix = (matrix / max_risk) * 100
        fmt = ".1f"
        cbar_label = "% of Maximum Risk"
    else:
        fmt = ".2f"
        cbar_label = "P&L ($)"

    df = pd.DataFrame(matrix, index=np.round(spot_range, 2), columns=[date.strftime('%b %d') for date in date_range])
    fig, ax = plt.subplots(figsize=(16, 10))

    sns.heatmap(df, annot=True, fmt=fmt, cmap="RdYlGn", 
                cbar_kws={'label': cbar_label}, ax=ax, linewidths=0.2, 
                center=0 if risk_display_type == "% of Maximum Risk" else entry_cost)

    st.write(f'{option_type} Entry cost: {entry_cost:.2f}')
    title = f"{option_type} Option P&L - Spot Price vs Date"
    if risk_display_type == "% of Maximum Risk":
        title += " (% of Max Risk)"
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Spot Price", fontsize=12)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    st.pyplot(fig)


def calculate_matrix(grid_size, expiration_date, start_date, S, K, r, 
                     sigma, option_type, spot_range, date_range, num_contracts, risk_display_type):
    matrix = np.zeros((grid_size, grid_size))
    max_risk = 0

    days_to_expiry = (expiration_date - start_date).days / 365.0
    initial_bs = BlackScholes(S, K, r, days_to_expiry, sigma)
    initial_price = initial_bs.call_price() if option_type == "Call" else initial_bs.put_price()

    entry_cost = initial_price * num_contracts * 100
    max_risk = entry_cost

    for i, spot in enumerate(spot_range):
        for j, date in enumerate(date_range):
            days_to_expiry = (expiration_date - date).days / 365.0
            if days_to_expiry <= 0:
                days_to_expiry = 0.0001  # avoid divide-by-zero in BS formula

            bs = BlackScholes(spot, K, r, days_to_expiry, sigma)
            if option_type == "Call":
                price = bs.call_price()
                intrinsic = max(0, spot - K)
            else:
                price = bs.put_price()
                intrinsic = max(0, K - spot)

            if date == expiration_date:
                pnl = (intrinsic - initial_price) * num_contracts * 100
            else:
                pnl = (price - initial_price) * num_contracts * 100

            matrix[i, j] = pnl
    
    display_heatmap(matrix, risk_display_type, max_risk, option_type, 
                    spot_range, date_range, entry_cost)

def create_matrix(start_date, days_diff, grid_size, expiration_date, num_contracts, 
                  spot_range, S, K, r, sigma, risk_display_type):
    date_range = [start_date + timedelta(days=int(i * days_diff / (grid_size-1))) for i in range(grid_size)]
    date_range[-1] = expiration_date  # last date is expiration date
    
    # Create columns for call and put
    col1, col2 = st.columns(2)

    for option_type, col in zip(["Call", "Put"], [col1, col2]):
        with col:
            calculate_matrix(grid_size, expiration_date, start_date, S, K, r, 
                             sigma, option_type, spot_range, date_range, num_contracts, risk_display_type)

def render_heatmap(S, K, t, sigma, r):
    st.title("P&L Heatmap by Spot price and Date")

    # Set date range
    today = datetime.now().date()
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        start_date = st.date_input("Start Date", today)
    with col_date2:
        expiration_date = st.date_input("Expiration Date", today + timedelta(days= t * 365))

    # Set spot price range
    grid_size = 15  # Number of steps in the grid
    col_spot1, col_spot2 = st.columns(2)
    with col_spot1:
        min_spot = st.number_input("Min Spot Price", value=round(S * 0.8, 2), step=1.0)
    with col_spot2:
        max_spot = st.number_input("Max Spot Price", value=round(S * 1.2, 2), step=1.0)

    spot_range = np.linspace(min_spot, max_spot, grid_size)

    # Calculation parameters
    num_contracts = st.slider("Number of Contracts (x100)", min_value=1, max_value=1000, value=1, step=1)
    risk_display_type = st.radio("Display", ["P&L Values", "% of Maximum Risk"], horizontal=True)

    days_diff = (expiration_date - start_date).days
   
    if days_diff <= 0:
        st.error("Expiration date must be after start date")
    else:
        create_matrix(start_date, days_diff, grid_size, expiration_date, num_contracts, spot_range, 
                      S, K, r, sigma, risk_display_type)
