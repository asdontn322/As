
# Quantum AI Trading Project

## Structure

- `bot/trading_bot.py`: Your LSTM-based trading bot
- `backend/main.py`: FastAPI server for predictions
- `dashboard/index.html`: Interactive frontend dashboard

## Instructions

### 1. Start Backend
```bash
cd backend
uvicorn main:app --reload
```

### 2. Run Bot
```bash
cd ../bot
python trading_bot.py
```

### 3. Open Dashboard
Open `dashboard/index.html` in your browser.
