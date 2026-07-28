# Oil & Gas Market Intelligence Automation

Automated Python pipeline that pulls live crude oil (WTI, Brent), natural gas prices, and US crude inventory data, analyzes daily/weekly movements, generates written market commentary, and produces a formatted Excel report — fully automated via Windows Task Scheduler.

## Features
- Live price data via `yfinance` (WTI Crude, Brent Crude, Natural Gas)
- US crude inventory data via EIA API
- Day-over-day % change, rolling 7/30-day averages, and volatility alerts
- Auto-generated written market commentary combining price and inventory trends
- Styled Excel report with conditional formatting for significant moves
- Fully automated daily execution with error handling for missing/incomplete data

## Pipeline
1. `save_prices.py` — pulls and stores daily commodity prices, handles duplicates
2. `get_inventory.py` — pulls and stores weekly EIA inventory data
3. `analyze_prices.py` — calculates metrics, flags significant moves, generates written commentary
4. `generate_report.py` — combines data table and commentary into a styled Excel report
5. `run_daily_report.py` — orchestrates the full pipeline with error handling
6. Scheduled daily via Windows Task Scheduler (`run_report.bat`)

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Get a free EIA API key at [eia.gov/opendata](https://www.eia.gov/opendata)
3. Add your key to `get_inventory.py`
4. Run `python run_daily_report.py`

## Data Sources
- Yahoo Finance (via yfinance)
- U.S. Energy Information Administration (EIA)

## Sample Output
*(Excel report screenshot below)*
