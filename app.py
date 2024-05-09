from flask import Flask, request, jsonify #flaskpackages
import requests #uliize requests package 

app = Flask(__name__)

# Dummy database to store trades
trades = []

# Alphavantage API key displayed here, no concern with exposure to public
API_KEY = '0C5BQZJGUFPO1Q45' #timeseriesweeklyaboutobecalled
STOCK_API_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={apikey}'

@app.route('/price/<symbol>')
def get_price(symbol):
    response = requests.get(STOCK_API_URL.format(symbol=symbol, apikey=API_KEY))
    data = response.json()
    # Parsing the weekly data, we assume that data['Weekly Time Series'] returns the latest week data.
    latest_week_data = list(data['Weekly Time Series'].values())[0]
    weekly_close = latest_week_data['4. close']
    return jsonify({symbol: weekly_close})

@app.route('/trade', methods=['POST'])
def record_trade():
    trade_info = request.json
    trades.append(trade_info)
    return jsonify({"status": "success", "trade": trade_info})

@app.route('/profits')
def calculate_profits():
    # Simple profit calculation
    total_profit = sum(t['profit'] for t in trades if 'profit' in t)
    return jsonify({"total_profit": total_profit})

if __name__ == '__main__':
    app.run(debug=True)
