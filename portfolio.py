import yfinance as yf


selection = ["NVDA", "AAPL", "GOOG", "ADBE"]
allocation = [0.3, 0.2, 0.4, 0.1]
init_position = 10000

# Assigns each respective stock its chosen weighting and then places them in alphabetical order so when the yfinance data comes back they can be assigned to the correct weights
weighted_portfolio = sorted([{"stock" : selection[i], "weight": allocation[i]} for i in range(len(selection))], key=lambda item: item["stock"])

portfolio = yf.download(selection, start="2012-01-01", end="2024-01-24")[['Adj Close']]

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

print(portfolio.head())
