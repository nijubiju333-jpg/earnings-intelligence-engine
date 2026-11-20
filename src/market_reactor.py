import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def calculate_abnormal_returns(ticker, event_date, days_before=10, days_after=10):
    """
    Calculates how a stock performs compared to the Nifty 50 (Market) 
    around an earnings event.
    """
    print(f"Analyzing {ticker} around {event_date.strftime('%Y-%m-%d')}...")
    
    # Set date range (adding buffer for calculations)
    start_date = (event_date - timedelta(days=days_before + 30)).strftime('%Y-%m-%d')
    end_date = (event_date + timedelta(days=days_after + 5)).strftime('%Y-%m-%d')
    
    # 1. Fetch Stock Data
    stock = yf.download(ticker, start=start_date, end=end_date, progress=False)
    # Fix for new yfinance MultiIndex columns
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)
    stock['Stock_Return'] = stock['Close'].pct_change()
    
    # 2. Fetch Nifty 50 Data (The Market Benchmark)
    nifty = yf.download("^NSEI", start=start_date, end=end_date, progress=False)
    if isinstance(nifty.columns, pd.MultiIndex):
        nifty.columns = nifty.columns.get_level_values(0)
    nifty['Market_Return'] = nifty['Close'].pct_change()
    
    # 3. Merge them together by Date
    df = pd.merge(stock[['Close', 'Stock_Return']], nifty[['Close', 'Market_Return']], 
                  left_index=True, right_index=True, how='left')
    df = df.dropna() # Remove empty rows
    
    # 4. Calculate Abnormal Return (The "Alpha")
    # Simple version: How much did the stock beat the market by today?
    df['Abnormal_Return'] = df['Stock_Return'] - df['Market_Return']
    
    # 5. Calculate Cumulative Abnormal Return (CAR)
    # This shows the total impact over the days following the event
    df['Cumulative_CAR'] = (1 + df['Abnormal_Return']).cumprod() - 1
    
    return df

# --- RUN THE TEST ---
if __name__ == "__main__":
    # Let's test TCS, which had a negative profit surprise in our data
    ticker = 'TCS.NS'
    event_date = datetime(2024, 1, 10) 
    
    results = calculate_abnormal_returns(ticker, event_date)
    
    print("\n--- Event Study Results (Last 10 Days) ---")
    # Show Date, Stock Return, Market Return, and the Abnormal Return
    print(results[['Stock_Return', 'Market_Return', 'Abnormal_Return', 'Cumulative_CAR']].tail(10))