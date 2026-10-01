# Signal Bot Demo

This project is a safe-start signal bot research project.

It includes:
- Binace public market data fetch
- EMA + RSI signal generation
- backtesting logic
- FastAPI endpoint

Important:
- This project is for learning and strategy testing only.
- It does not guarantee profit.
- It does not automatically trade real money.

## Setup

```bash
pip install -r requirements.txt
```

### Run
```bash
uvicorn app.main:app --reload
```

### Test endpoints
```bash
curl "http://127.0.0.1:8000/signal?symbol=BTCUSDT&interval=1h&limit=200"
curl "http://127.0.0.1:8000/backtest?symbol=BTCUSDT&interval=1h&limit=500"
```

## Disclaimer
This project is not trading advice. Historical signals do not guarantee future profits.
