import yfinance as yf
import matplotlib.pyplot as plt


selection = ["NVDA", "AAPL", "GOOG", "ADBE"]
allocation = [0.3, 0.2, 0.4, 0.1]
init_position = 10000
start_date = "2023-01-01"
end_date = "2024-01-24"

# Assigns each respective stock its chosen weighting and then places them in alphabetical order so when the yfinance data comes back they can be assigned to the correct weights
weighted_portfolio = sorted([{"stock" : selection[i], "weight": allocation[i]} for i in range(len(selection))], key=lambda item: item["stock"])

portfolio = yf.download(selection, start=start_date, end=end_date)[['Adj Close']]

# Compute normalised returns for each stock
for index, ticker in enumerate(portfolio.columns):
    norm_return_col = f"Norm. Return {ticker[1]}"
    alloc_return_col = f"Alloc Return {ticker[1]}"

    norm_returns = portfolio[ticker] / portfolio[ticker].iloc[0]
    portfolio[norm_return_col] = norm_returns

    portfolio[alloc_return_col] = norm_returns * weighted_portfolio[index]["weight"]

del allocation, index, selection, ticker, norm_returns, alloc_return_col, norm_return_col
portfolio = portfolio.filter(like="Alloc", axis=1)

#Compute portfolio value of initial amount invested over lifetime
portfolio['Total Position'] = init_position * portfolio.sum(axis=1)


#Compute portfolio statistics
rfr = yf.Ticker("^FVX")
portfolio['Daily Return'] = portfolio['Total Position'].pct_change(1)
sharpe_ratio = (252**0.5)*((portfolio['Daily Return'].mean() - rfr.info['previousClose']) / portfolio['Daily Return'].std())

print(portfolio.head())
