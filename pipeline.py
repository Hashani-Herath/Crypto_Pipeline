import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

def run_crypto_pipeline():
    # 1. THE ADDRESS OF THE DATA (API URL)
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,solana,cardano",
        "order": "market_cap_desc"
    }
    
    try:
        print("Step 1: Fetching data from the internet...")
        response = requests.get(url, params=params)
        response.raise_for_status() # Make sure the internet connection worked
        raw_data = response.json()
        
        # 2. THE CLEANING PHASE (Transformation)
        print("Step 2: Cleaning and structuring data...")
        cleaned_records = []
        for coin in raw_data:
            record = {
                "fetched_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                "coin_name": coin["name"],
                "symbol": coin["symbol"].upper(),
                "price_usd": coin["current_price"],
                "market_cap": coin["market_cap"],
                "volume_24h": coin["total_volume"]
            }
            cleaned_records.append(record)
            
        # Convert into a structured table format (DataFrame)
        df = pd.DataFrame(cleaned_records)
        print(df)
        return df

    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        return None

if __name__ == "__main__":
    run_crypto_pipeline()


def save_to_database(df):
    print("Step 3: Saving data into PostgreSQL...")
    # Connect to the Docker database we set up
    engine = create_engine('postgresql://postgres:my_secret_password@localhost:5432/postgres')
    
    # Append the rows to our table
    df.to_sql('crypto_prices', engine, if_exists='append', index=False)
    print("✔ Success! Data successfully stored.")

# Run the full pipeline
if __name__ == "__main__":
    market_data = run_crypto_pipeline()
    if market_data is not None:
        save_to_database(market_data)