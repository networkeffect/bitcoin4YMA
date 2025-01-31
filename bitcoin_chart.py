import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import os

print("🔄 Script started...")

# Define data file path
file_path = "btc_prices.csv"

# Step 1: Check if data is already saved
if os.path.exists(file_path):
    print("📂 Loading data from local CSV...")
    
    # Skip the first two rows to handle incorrect headers
    btc = pd.read_csv(file_path, skiprows=2)
    
    print("📄 Columns found in CSV:", btc.columns)

    # Ensure 'Date' is set as index
    if "Date" in btc.columns:
        btc["Date"] = pd.to_datetime(btc["Date"])  # Convert to datetime
        btc.set_index("Date", inplace=True)
        print("✅ Date column set as index.")
    else:
        print("❌ 'Date' column not found. Deleting and re-downloading the CSV...")
        os.remove(file_path)  # Delete corrupted file
        exit()
else:
    print("🌐 Downloading Bitcoin price data from Yahoo Finance...")
    try:
        btc = yf.download('BTC-USD', start='2015-01-01', end='2025-01-01', progress=False)
        print("📄 Available columns in BTC DataFrame:", btc.columns)

        if btc.empty:
            print("⚠️ No data retrieved! Possible API issue or no data available for the selected date range.")
            exit()

        btc.to_csv(file_path, index=True)  # Ensure 'Date' column is included
        print("✅ Data downloaded and saved as 'btc_prices.csv'.")
    except Exception as e:
        print(f"❌ Error downloading data: {e}")
        exit()

# Use 'Close' instead of 'Adj Close' if necessary
price_column = 'Adj Close' if 'Adj Close' in btc.columns else 'Close'
print(f"📊 Using column '{price_column}' for price data.")

# Calculate 4-year moving average
btc['4Y_MA'] = btc[price_column].rolling(window=1460, min_periods=1).mean()
print("✅ 4-Year Moving Average calculated.")

# Step 3: Plot Bitcoin price and moving average
print("📈 Creating the plot...")
plt.figure(figsize=(12, 6))
plt.plot(btc.index, btc[price_column], label='Bitcoin Price (USD)', color='blue', alpha=0.6)
plt.plot(btc.index, btc['4Y_MA'], label='4-Year Moving Average', color='red', linewidth=2)

# Apply logarithmic scale on Y-axis
plt.yscale('log')

# Labels and formatting
plt.xlabel('Date')
plt.ylabel('Price (USD, Log Scale)')
plt.title('Bitcoin Price with 4-Year Moving Average (Log Scale)')
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

print("🖼️ Displaying the chart...")
plt.show()

print("✅ Script execution completed successfully!")
