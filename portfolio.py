import yfinance as yf


selection = ["NVDA", "AAPL", "GOOG", "ADBE"]
allocation = [0.3, 0.2, 0.4, 0.1]
test = [{"stock" : selection[i], "allocation": allocation[i]} for i in range(len(selection))]
portfolio = yf.download(selection, start="2012-01-01", end="2024-01-24")[['Adj Close']]


i = 0
# Compute normalised returns for each stock
print(portfolio.columns)
for ticker in portfolio.columns:
    normalised_returns = []
    alloc_returns = []
    for price in (portfolio[ticker]):
        normalised_returns.append(price / portfolio[ticker].iloc[0])
    portfolio[f"Norm. Return {ticker[1]} "] = normalised_returns

    for price in normalised_returns:
        # print('normalised return ', price)
        alloc_returns.append(price*allocation[i])
    portfolio[f"Alloc. Return {ticker[1]} "] = alloc_returns

    i += 1

print(portfolio.head())
