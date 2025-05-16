# def fetch_nifty50_data():
#     url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=YYIOQCNUTV2SGSBC'
#     home_url = 'https://www.nseindia.com'

#     session = requests.Session()
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#         "Accept-Language": "en-US,en;q=0.9",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept": "application/json",
#         "Referer": "https://www.nseindia.com/",
#         "Connection": "keep-alive"
#     }
#     session.headers.update(headers)

#     try:
#         # Visit homepage to get necessary cookies
#         response = session.get(home_url, timeout=10)
#         response.raise_for_status()
#         time.sleep(1)

#         # Now access the API with session and cookies
#         response = session.get(url, timeout=10)
#         if response.status_code == 200:demo
#             data = response.json()
#             df = pd.DataFrame(data['data'])

#             for col in ['pChange', 'yearHigh', 'yearLow', 'lastPrice']:
#                 df[col] = pd.to_numeric(df[col], errors='coerce')

#             return df
#         else:
#             print(f"Failed to fetch data: Status code {response.status_code}")

#     except Exception as e:
#         print(f"Error occurred: {e}")

#     return None


















import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

def fetch_nifty50_data():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=YYIOQCNUTV2SGSBC'
    home_url = 'https://www.nseindia.com'
    # url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'
    max_retries = 3
    retry_delay = 5

    session = requests.Session()
    session.headers.update(get_headers())

    for attempt in range(max_retries):
        try:
            session.get("https://www.nseindia.com", headers=get_headers())
            time.sleep(2)  # Delay to avoid being blocked
            response = session.get(url)

            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data['data'])

                # Convert data types safely
                for col in ['pChange', 'yearHigh', 'yearLow', 'lastPrice']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

                return df
            else:
                print(f"Failed to fetch data: Status code {response.status_code}")

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

    return None

def analyze_data(df):
    gainers = df.nlargest(5, 'pChange')[['symbol', 'pChange']]
    losers = df.nsmallest(5, 'pChange')[['symbol', 'pChange']]

    # Fixing high/low calculations
    df['high_diff'] = ((df['lastPrice'] - df['yearHigh']) / df['yearHigh'].replace(0, np.nan)) * 100
    df['low_diff'] = ((df['lastPrice'] - df['yearLow']) / df['yearLow'].replace(0, np.nan)) * 100

    below_high = df[df['high_diff'] <= -30].nlargest(5, 'high_diff')[['symbol', 'high_diff']]
    above_low = df[df['low_diff'] >= 20].nlargest(5, 'low_diff')[['symbol', 'low_diff']]

    # Plotting
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.bar(gainers['symbol'], gainers['pChange'], color='green')
    plt.title('Top 5 Gainers')
    plt.xticks(rotation=45)

    plt.subplot(1, 2, 2)
    plt.bar(losers['symbol'], losers['pChange'], color='red')
    plt.title('Top 5 Losers')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('gainers_losers.png', dpi=300, bbox_inches='tight')
    plt.close()

    return gainers, losers, below_high, above_low

def main():
    df = fetch_nifty50_data()
    if df is not None:
        gainers, losers, below_high, above_low = analyze_data(df)

        print("\nTop 5 Gainers:")
        print(gainers)
        print("\nTop 5 Losers:")
        print(losers)
        print("\nStocks 30% below 52-week high:")
        print(below_high)
        print("\nStocks 20% above 52-week low:")
        print(above_low)
    else:
        print("Failed to retrieve NIFTY 50 data.")

if __name__ == "__main__":
    main()


