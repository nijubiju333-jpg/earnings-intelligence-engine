import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def calculate_event_study(ticker, event_date, window_days=5):
    """Calculates 5-day Cumulative Abnormal Return (CAR) for a stock."""
    start_date = (event_date - timedelta(days=15)).strftime('%Y-%m-%d')
    end_date = (event_date + timedelta(days=window_days + 5)).strftime('%Y-%m-%d')
    
    try:
        # 1. Get Stock Data
        stock = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if isinstance(stock.columns, pd.MultiIndex):
            stock.columns = stock.columns.get_level_values(0)
        stock['Stock_Return'] = stock['Close'].pct_change()
        
        # 2. Get Nifty 50 Data (Market Benchmark)
        nifty = yf.download("^NSEI", start=start_date, end=end_date, progress=False)
        if isinstance(nifty.columns, pd.MultiIndex):
            nifty.columns = nifty.columns.get_level_values(0)
        nifty['Market_Return'] = nifty['Close'].pct_change()
        
        # 3. Merge and Calculate Abnormal Return
        df = pd.merge(stock[['Stock_Return']], nifty[['Market_Return']], 
                      left_index=True, right_index=True, how='left').dropna()
        
        df['Abnormal_Return'] = df['Stock_Return'] - df['Market_Return']
        
        # 4. Calculate Cumulative Abnormal Return (CAR)
        event_mask = df.index >= event_date
        car = (1 + df.loc[event_mask, 'Abnormal_Return']).cumprod() - 1
        
        if len(car) > window_days:
            return car.iloc[window_days]
        elif len(car) > 0:
            return car.iloc[-1]
        else:
            return 0.0
            
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return 0.0

# --- MASTER ENGINE LOOP ---
if __name__ == "__main__":
    print("Starting Peer Comparison Engine (Infosys vs Wipro)...")
    
    # Load Data
    earnings_df = pd.read_csv('data/earnings_dates_sample.csv')
    earnings_df['announcement_date'] = pd.to_datetime(earnings_df['announcement_date'])
    
    # FIX: Calculate the profit surprise percentage right here!
    earnings_df['profit_surprise_pct'] = ((earnings_df['actual_net_profit_cr'] - earnings_df['expected_net_profit_cr']) / earnings_df['expected_net_profit_cr']) * 100
    
    # FILTER: Only keep Infosys and Wipro
    target_tickers = ['INFY.NS', 'WIPRO.NS']
    earnings_df = earnings_df[earnings_df['ticker'].isin(target_tickers)]
    
    results = []
    
    print("Processing peer comparison...")
    for index, row in earnings_df.iterrows():
        ticker = row['ticker']
        date = row['announcement_date']
        profit_surprise = row['profit_surprise_pct']
        
        print(f"Analyzing {ticker} for {date.strftime('%Y-%m-%d')}...")
        
        # Calculate 5-day Cumulative Abnormal Return
        car_5day = calculate_event_study(ticker, date, window_days=5)
        
        results.append({
            'Ticker': ticker,
            'Date': date.strftime('%Y-%m-%d'),
            'Profit_Surprise_%': round(profit_surprise, 2),
            '5-Day_CAR_%': round(car_5day * 100, 2) # Convert to percentage
        })
        
    # Save and Print Results
    final_df = pd.DataFrame(results)
    final_df.to_csv('data/peer_comparison_results.csv', index=False)
    
    print("\n--- PEER COMPARISON COMPLETE ---")
    print(final_df.to_string(index=False))