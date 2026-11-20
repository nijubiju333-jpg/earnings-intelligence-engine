import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def load_earnings_data(filepath):
    """Loads the earnings data and calculates the surprise percentage."""
    print("Loading earnings data...")
    df = pd.read_csv(filepath)
    df['announcement_date'] = pd.to_datetime(df['announcement_date'])
    
    # Calculate how much the company beat or missed expectations
    df['revenue_surprise_pct'] = ((df['actual_revenue_cr'] - df['expected_revenue_cr']) / df['expected_revenue_cr']) * 100
    df['profit_surprise_pct'] = ((df['actual_net_profit_cr'] - df['expected_net_profit_cr']) / df['expected_net_profit_cr']) * 100
    
    return df

def get_stock_data(ticker, event_date, days_before=10, days_after=10):
    """Downloads stock price data around the earnings date."""
    print(f"Fetching stock data for {ticker}...")
    
    # Calculate the date range to download
    start_date = (event_date - timedelta(days=days_before)).strftime('%Y-%m-%d')
    end_date = (event_date + timedelta(days=days_after)).strftime('%Y-%m-%d')
    
    try:
        # Download data from Yahoo Finance
        stock = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        # Calculate daily percentage change in stock price
        stock['Daily_Return'] = stock['Close'].pct_change()
        
        return stock
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# --- THIS PART RUNS THE CODE ---
if __name__ == "__main__":
    # 1. Load the CSV file we created
    earnings_df = load_earnings_data('data/earnings_dates_sample.csv')
    
    # Print the first few rows to see our surprises
    print("\n--- Earnings Surprises ---")
    print(earnings_df[['ticker', 'company_name', 'revenue_surprise_pct', 'profit_surprise_pct']].head())
    
    # 2. Test fetching stock data for the very first company in the list
    first_company = earnings_df.iloc[0]
    ticker = first_company['ticker']
    date = first_company['announcement_date']
    
    print(f"\n--- Testing Stock Download for {ticker} on {date.strftime('%Y-%m-%d')} ---")
    stock_data = get_stock_data(ticker, date)
    
    if stock_data is not None:
        print("\nSuccessfully downloaded stock data! Here are the last 3 days:")
        print(stock_data[['Close', 'Daily_Return']].tail(3))