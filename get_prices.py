import yfinance as yf

# Ticker symbols: CL=F is WTI Crude, BZ=F is Brent Crude, NG=F is Natural Gas
tickers = {
    "WTI Crude": "CL=F",
    "Brent Crude": "BZ=F",
    "Natural Gas": "NG=F"
}

for name, symbol in tickers.items():
    data = yf.Ticker(symbol).history(period="5d")
    print(f"\n--- {name} ({symbol}) ---")
    print(data[["Close"]])