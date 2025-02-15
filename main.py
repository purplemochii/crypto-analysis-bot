import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from flask import Flask

# Initialize the Kraken exchange bc regular ccxt doesn't work in IE. if elsewhere, use ccxt
exchange = ccxt.kraken()

# Fetch market data (historical) from ccxt library
symbol = 'BTC/EUR'
timeframe = '1h'
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

# Convert to a DataFrame for easier handling
df = pd.DataFrame(
    ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Print a preview of historical data (first few rows)
print(df.head())

# Fetch ticker data for the symbol
ticker = exchange.fetch_ticker(symbol)


# Sentiment analysis function
def analyze_and_trade(texts):
  total_polarity = 0
  for text in texts:
    analysis = TextBlob(text)
    # Accumulate polarity
    total_polarity += analysis.sentiment.polarity

  average_polarity = total_polarity / len(texts)

  # Determine sentiment and trading signal
  if average_polarity > 0:
    sentiment = f"Sentiment: Polarity = {average_polarity:.2f}                       (Positive)"
    signal = "Buy signal"
  else:
    sentiment = f"Sentiment: Polarity = {average_polarity:.2f}                       (Negative)"
    signal = "Sell signal"

  return sentiment, signal


# Example usage with multiple news items
news_headlines = [
    "The market is looking great today!",
    "There are some concerns about market volatility.",
    "Investors are optimistic about Bitcoin's future."
]

# Analyze a list of news headlines
sentiment, signal = analyze_and_trade(news_headlines)

# Extract relevant ticker details
symbol = ticker['symbol']
high = ticker['high']
low = ticker['low']
bid = ticker['bid']
ask = ticker['ask']
last = ticker['last']
change = ticker['change']
percentage = ticker['percentage']
base_volume = ticker['baseVolume']
quote_volume = ticker['quoteVolume']

# Printing the nicely formatted output; very mindful, very demure lol
print(f"\nMarket Data for {symbol}")
print("-" * 30)
print(f"High Price: {high}")
print(f"Low Price: {low}")
print(f"Bid Price: {bid}")
print(f"Ask Price: {ask}")
print(f"Last Trade Price: {last}")
print(f"Change: {change} ({percentage:.2f}%)")
print(f"Base Volume (BTC): {base_volume}")
print(f"Quote Volume (EUR): {quote_volume}")
print("-" * 30)
print(f"{sentiment}")
print(f"{signal}")
print("\n")

# let's backtest!!!!!
# Generate a signal: Buy if closing price is above the average of the high and low
df['signal'] = df['close'] > ((df['high'] + df['low']) / 2)

# Calculate returns if you bought when the signal was True
df['strategy_return'] = df['signal'].shift(1) * (df['close'].pct_change())

# Calculate cumulative returns
df['cumulative_strategy_return'] = (1 + df['strategy_return']).cumprod()

# Plot the strategy performance
plt.figure(figsize=(10, 6))
df['cumulative_strategy_return'].plot(
    title='Cumulative Returns of the Strategy')
plt.show()

# This will list all the supported symbols
markets = exchange.load_markets()
print(markets.keys())
