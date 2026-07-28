import yfinance as yf
import pandas as pd
from datetime import datetime
import os

tickers = {
    "WTI Crude": "CL=F",
    "Brent Crude": "BZ=F",
    "Natural Gas": "NG=F"
}

today = datetime.now().strftime("%Y-%m-%d")
rows = []

for name, symbol in tickers.items():
    data = yf.Ticker(symbol).history(period="1d")
    if not data.empty:
        close_price = data["Close"].iloc[-1]
        rows.append({"Date": today, "Commodity": name, "Ticker": symbol, "Close": round(close_price, 2)})

new_data = pd.DataFrame(rows)

file_path = "price_history.csv"

if os.path.exists(file_path):
    existing_data = pd.read_csv(file_path)
    combined = pd.concat([existing_data, new_data], ignore_index=True)
    combined = combined.drop_duplicates(subset=["Date", "Commodity"], keep="last")
else:
    combined = new_data

combined.to_csv(file_path, index=False)
print(f"Saved {len(new_data)} rows for {today}")
print(combined.tail(10))