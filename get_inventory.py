import requests
import pandas as pd
from datetime import datetime

API_KEY = "64OC4lAqt4m6eyqVkfoRnEMazN8aUs4N19I1uaze"

url = "https://api.eia.gov/v2/petroleum/stoc/wstk/data/"

params = {
    "api_key": API_KEY,
    "frequency": "weekly",
    "data[0]": "value",
    "facets[series][]": "WCESTUS1",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "length": 5
}

response = requests.get(url, params=params)
result = response.json()

records = result["response"]["data"]
df = pd.DataFrame(records)
print(df[["period", "value", "units"]])
import os

file_path = "inventory_history.csv"
new_data = df[["period", "value", "units"]].rename(columns={"period": "Date", "value": "Inventory_MBBL"})

if os.path.exists(file_path):
    existing_data = pd.read_csv(file_path)
    combined = pd.concat([existing_data, new_data], ignore_index=True)
    combined = combined.drop_duplicates(subset=["Date"], keep="last")
else:
    combined = new_data

combined.to_csv(file_path, index=False)
print(f"\nSaved to {file_path}")