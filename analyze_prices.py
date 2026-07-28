import pandas as pd

file_path = "price_history.csv"
df = pd.read_csv(file_path)

inventory_path = "inventory_history.csv"
try:
    inv_df = pd.read_csv(inventory_path)
    inv_df["Date"] = pd.to_datetime(inv_df["Date"])
    inv_df = inv_df.sort_values("Date").reset_index(drop=True)

    if len(inv_df) >= 2:
        latest_inv = inv_df.iloc[-1]
        previous_inv = inv_df.iloc[-2]
        inv_change = latest_inv["Inventory_MBBL"] - previous_inv["Inventory_MBBL"]
        inv_change_label = "Build" if inv_change > 0 else "Draw" if inv_change < 0 else "Unchanged"
    else:
        latest_inv = inv_df.iloc[-1] if len(inv_df) == 1 else None
        inv_change = None
        inv_change_label = "N/A"
except (FileNotFoundError, IndexError):
    latest_inv = None
    inv_change = None
    inv_change_label = "N/A"

# Make sure Date is treated as an actual date, not text
df["Date"] = pd.to_datetime(df["Date"])

results = []

for commodity in df["Commodity"].unique():
    subset = df[df["Commodity"] == commodity].sort_values("Date").reset_index(drop=True)

    if len(subset) < 2:
        print(f"Not enough history yet for {commodity} (need at least 2 days) — skipping analysis.")
        continue

    latest = subset.iloc[-1]
    previous = subset.iloc[-2]

    day_change = latest["Close"] - previous["Close"]
    day_change_pct = (day_change / previous["Close"]) * 100

    rolling_7 = subset["Close"].tail(7).mean()
    rolling_30 = subset["Close"].tail(30).mean()

    alert = "⚠️ BIG MOVE" if abs(day_change_pct) >= 3 else ""

    results.append({
        "Commodity": commodity,
        "Latest Close": round(latest["Close"], 2),
        "Day Change": round(day_change, 2),
        "Day Change %": round(day_change_pct, 2),
        "7-Day Avg": round(rolling_7, 2),
        "30-Day Avg": round(rolling_30, 2),
        "Alert": alert
    })

# Add inventory row to results BEFORE building the summary DataFrame
if latest_inv is not None:
    results.append({
        "Commodity": "US Crude Inventories",
        "Latest Close": f"{int(latest_inv['Inventory_MBBL']):,} MBBL",
        "Day Change": f"{int(inv_change):+,} MBBL" if inv_change is not None else "N/A",
        "Day Change %": inv_change_label,
        "7-Day Avg": "-",
        "30-Day Avg": "-",
        "Alert": "⚠️ LARGE BUILD" if inv_change is not None and inv_change > 3000 else ("⚠️ LARGE DRAW" if inv_change is not None and inv_change < -3000 else "")
    })

# Build summary AFTER all rows (price + inventory) are in results
summary = pd.DataFrame(results)

print("\n=== Daily Market Summary ===\n")
print(summary.to_string(index=False))

summary.to_csv("daily_summary.csv", index=False)
print(f"\nSaved summary to daily_summary.csv")

commentary_lines = []
commentary_lines.append(f"Market Commentary — {pd.Timestamp.today().strftime('%Y-%m-%d')}")
commentary_lines.append("")

for row in results:
    if row["Commodity"] == "US Crude Inventories":
        continue
    commodity = row["Commodity"]
    change_pct = row["Day Change %"]
    latest = row["Latest Close"]
    avg30 = row["30-Day Avg"]

    direction = "rose" if change_pct > 0 else "fell" if change_pct < 0 else "was flat"
    magnitude = "sharply" if abs(change_pct) >= 3 else "modestly" if abs(change_pct) >= 1 else "slightly"

    vs_avg = "above" if latest > avg30 else "below" if latest < avg30 else "in line with"

    sentence = (
        f"{commodity} {direction} {magnitude} today, closing at {latest}, "
        f"a {abs(change_pct)}% move. This puts it {vs_avg} its 30-day average of {avg30}."
    )
    commentary_lines.append(sentence)

# Inventory sentence added ONCE, after the loop finishes — not inside it
if latest_inv is not None and inv_change is not None:
    inv_sentence = (
        f"US crude inventories showed a {inv_change_label.lower()} of {abs(int(inv_change)):,} thousand barrels "
        f"in the week ending {latest_inv['Date'].strftime('%Y-%m-%d')}, bringing total stocks to "
        f"{int(latest_inv['Inventory_MBBL']):,} MBBL."
    )
    commentary_lines.append(inv_sentence)

commentary_text = "\n".join(commentary_lines)
print("\n" + commentary_text)

with open("market_commentary.txt", "w", encoding="utf-8") as f:
    f.write(commentary_text)

print("\nSaved commentary to market_commentary.txt")