import yfinance as yf


selection = ["NVDA", "AAPL", "GOOG", "ADBE"]
allocation = [0.3, 0.2, 0.4, 0.1]

# Assigns each respective stock its chosen weighting and then places them in alphabetical order so when the yfinance data comes back they can be assigned to the correct weights
weighted_portfolio = sorted([{"stock" : selection[i], "weight": allocation[i]} for i in range(len(selection))], key=lambda item: item["stock"])

portfolio = yf.download(selection, start="2012-01-01", end="2024-01-24")[['Adj Close']]

i = 0
# Compute normalised returns for each stock
for ticker in portfolio.columns:
    normalised_returns = []
    alloc_returns = []
    for price in (portfolio[ticker]):
        normalised_returns.append(price / portfolio[ticker].iloc[0])
    portfolio[f"Norm. Return {ticker[1]} "] = normalised_returns

    for price in normalised_returns:
        alloc_returns.append(price*weighted_portfolio[i]["weight"])
    portfolio[f"Alloc. Return {ticker[1]} "] = alloc_returns

    i += 1

print(portfolio.head())
