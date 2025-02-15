from flask import Flask, render_template, jsonify
import ccxt
from textblob import TextBlob

app = Flask(__name__)

# Initialize the Kraken exchange
exchange = ccxt.kraken()

# Define the symbol and timeframe (e.g., 1h for 1-hour candles)
symbol = 'BTC/EUR'
timeframe = '1h'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/market-data')
def market_data():
    # Fetch ticker data for BTC/EUR (or any other symbol you choose)
    ticker = exchange.fetch_ticker(symbol)

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

    data = {
        'symbol': ticker['symbol'],
        'high': ticker['high'],
        'low': ticker['low'],
        'bid': ticker['bid'],
        'ask': ticker['ask'],
        'last': ticker['last'],
        'change': ticker['change'],
        'percentage': ticker['percentage'],
        'base_volume': ticker['baseVolume'],
        'quote_volume': ticker['quoteVolume'],
        'sentiment': sentiment
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
