import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import asyncio
import websockets
import json
import requests
from datetime import datetime

class QuantumAITradingBot:
    def __init__(self, websocket_url="wss://api.example.com/market-data"):
        self.websocket_url = websocket_url
        self.model = self._build_model()
        self.scaler = MinMaxScaler()
        self.data = []
        self.is_trained = False

    def _build_model(self):
        model = Sequential([
            LSTM(100, return_sequences=True, input_shape=(60, 1)),
            Dropout(0.2),
            LSTM(50),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def preprocess_data(self, data, fit_scaler=False):
        prices = np.array([d['price'] for d in data]).reshape(-1, 1)
        if fit_scaler:
            scaled_prices = self.scaler.fit_transform(prices)
        else:
            scaled_prices = self.scaler.transform(prices)
        X = []
        for i in range(60, len(scaled_prices)):
            X.append(scaled_prices[i-60:i])
        return np.array(X)

    def prepare_targets(self, data):
        prices = np.array([d['price'] for d in data]).reshape(-1, 1)
        return self.scaler.transform(prices[60:])  # Skip first 60 like X

    async def connect_websocket(self):
        while True:
            try:
                async with websockets.connect(self.websocket_url) as ws:
                    print("WebSocket connected.")
                    while True:
                        message = await ws.recv()
                        data_point = json.loads(message)
                        self.data.append(data_point)
                        if len(self.data) > 100:
                            self.data = self.data[-100:]

                        if self.is_trained and len(self.data) >= 60:
                            X = self.preprocess_data(self.data[-61:], fit_scaler=False)
                            prediction = self.model.predict(X[-1:])
                            scaled_prediction = self.scaler.inverse_transform(prediction)
                            print(f"Predicted price: {scaled_prediction[0][0]:.2f}")

                            # Send to backend
                            time_now = datetime.utcnow().strftime("%H:%M:%S")
                            requests.post("http://localhost:8000/prediction", json={
                                "time": time_now,
                                "price": data_point['price'],
                                "prediction": float(scaled_prediction[0][0]),
                                "confidence": float(np.random.uniform(0.7, 0.99))
                            })
            except Exception as e:
                print(f"WebSocket error: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)

    def train_model(self, historical_data):
        if len(historical_data) < 61:
            raise ValueError("Need at least 61 data points for training")

        X = self.preprocess_data(historical_data, fit_scaler=True)
        y = self.prepare_targets(historical_data)
        self.model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)
        self.is_trained = True
        print("Model trained successfully.")

async def main():
    bot = QuantumAITradingBot()
    # Load your historical training data here before connecting
    # bot.train_model(historical_data)
    await bot.connect_websocket()

if __name__ == "__main__":
    asyncio.run(main())
                                                   
