# 📊 Earnings Intelligence & Stock Reaction Engine

A quantitative research engine built with Python that analyzes how equity markets react to corporate earnings announcements. This project moves beyond simple stock price tracking by applying academic **Event Study Methodology** to calculate **Abnormal Returns** and **Cumulative Abnormal Returns (CAR)**.

## 🎯 Project Objective
To determine whether the stock market efficiently prices in earnings surprises, and to identify anomalies where stocks significantly outperform or underperform the broader market (Nifty 50) following quarterly results.

## 🛠️ Key Features
* **Automated Data Pipeline:** Fetches historical stock prices and Nifty 50 benchmark data via `yfinance`.
* **Earnings Surprise Calculation:** Quantifies the difference between expected and actual financial results.
* **Event Study Methodology:** Calculates daily Abnormal Returns (Stock Return - Market Return) to isolate the specific impact of the earnings event.
* **Peer Comparison:** Head-to-head analysis of direct competitors (e.g., Infosys vs. Wipro) during identical market cycles.

## 📐 Methodology
1. **Event Window:** Analyzes stock performance 5 days post-earnings announcement.
2. **Benchmark:** Uses the Nifty 50 Index (^NSEI) to calculate market-adjusted returns.
3. **Metric:** Cumulative Abnormal Return (CAR) = (1 + Daily Abnormal Return).cumprod() - 1.

## 📊 Key Findings (Infosys vs. Wipro)
The engine revealed interesting market inefficiencies during the Q2/Q3 FY24 earnings season:
* **Infosys (Jan 11, 2024):** Despite a **-1.28% negative profit surprise**, the stock generated a massive **+8.89% 5-Day CAR**. This suggests the market had overly pessimistic expectations priced in.
* **Wipro (Oct 18, 2023):** A **-4.84% profit miss** resulted in a **-3.39% CAR**, showing the market efficiently punished the stock for underperformance.

*(See `data/peer_comparison_chart.png` for the full visual analysis)*

## 🚀 How to Run
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment and install dependencies: `pip install pandas yfinance matplotlib seaborn`
4. Run the research engine: `python src/research_engine.py`
5. Generate visualizations: `python src/visualizer.py`

## 📁 Project Structure
* `src/data_fetcher.py`: Handles raw data ingestion.
* `src/market_reactor.py`: Calculates daily abnormal returns.
* `src/research_engine.py`: The master loop that processes multiple tickers.
* `src/visualizer.py`: Generates professional Seaborn/Matplotlib charts.
* `data/`: Contains raw CSV inputs and generated outputs.

## 🧠 Technologies Used
Python, Pandas, NumPy, yfinance, Matplotlib, Seaborn, Event Study Methodology.