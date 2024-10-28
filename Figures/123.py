import yfinance as yf
import pandas as pd

# Define the cryptocurrencies with their Yahoo Finance ticker symbols
symbols = ["ATOM-USD", "aave-USD", "gno-usd", "btc-usd"]

# Download historical data for the past 3 years
data = yf.download(symbols, start="2019-09-01", end="2024-10-01")["Adj Close"]

# Calculate daily returns for each cryptocurrency
returns = data.pct_change()

# Calculate the correlation matrix
correlation_matrix = returns.corr()

# Display the correlation matrix
print("3-Year Cryptocurrency Price Correlation:")
print(correlation_matrix)