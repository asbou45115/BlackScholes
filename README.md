# Black-Scholes pricing model

Check out the project at [black-scholes-asbou45115.streamlit.app](https://black-scholes-asbou45115.streamlit.app)

### 📈 Black-Scholes Option P&L Heatmap
This is a Streamlit app that visualizes the Profit & Loss (P&L) of call and put options across a range of spot prices and dates using the Black-Scholes model.

🚀 Features
- 📅 Select custom start and expiration dates
- 💰 Set ranges for spot prices, number of contracts, and volatility
- 🧠 Choose between P&L in dollars or as a % of maximum risk
- 🧊 Interactive heatmaps for both Call and Put options
- 🧮 Displays Black-Scholes formulas and explanations
- 📚 Educational and visual aid for options trading concepts

🧠 How it Works
The app uses the Black-Scholes model to compute option prices over a grid of:
- Spot prices (S)
- Dates until expiration (t)
- It then calculates the P&L relative to the entry price and visualizes the results using Seaborn heatmaps.
- At expiration, the P&L is calculated using the intrinsic value. For earlier dates, the current theoretical option price is used.

📦 Installation
1. Clone the repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. To run the app locally:
```
streamlit run black_scholes_app.py
```
**This project is for educational purposes only and does not constitute financial advice.**
