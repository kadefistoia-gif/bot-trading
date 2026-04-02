import time
import json
from datetime import datetime, timedelta
from config import *

from binance.client import Client  # pip install python-binance
import numpy as np
import pandas as pd

# --- SETUP DEMO ---
API_KEY = ""  # dejar vacío para demo
API_SECRET = ""
client = Client(API_KEY, API_SECRET, testnet=True)

FILE = "data.json"

# cargar datos previos
try:
    with open(FILE, "r") as f:
        trades_data = json.load(f)
except:
    trades_data = []

# Funciones auxiliares
def get_ohlc(symbol, interval, limit):
    """Trae velas OHLC desde Binance y devuelve DataFrame"""
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        "open_time","open","high","low","close","volume",
        "close_time","quote_asset_volume","trades",
        "taker_base_vol","taker_quote_vol","ignore"
    ])
    df = df.astype({"open":"float","high":"float","low":"float","close":"float"})
    return df[["open","high","low","close"]]

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def find_divergence(df):
    """Detecta divergencia en RSI en H1 según reglas"""
    rsi = compute_rsi(df["close"], RSI_PERIOD)
    highs_idx = df["close"].iloc[-DIV_LOOKBACK:].idxmax()
    lows_idx = df["close"].iloc[-DIV_LOOKBACK:].idxmin()
    # Alcista: precio hace mínimo más bajo, RSI mínimo más alto
    if df["close"].iloc[lows_idx] < df["close"].iloc[-DIV_LOOKBACK] and rsi.iloc[lows_idx] > rsi.iloc[-DIV_LOOKBACK]:
        if rsi.iloc[lows_idx] <= RSI_LOW:
            return "long", lows_idx
    # Bajista: precio hace máximo más alto, RSI máximo más bajo
    if df["close"].iloc[highs_idx] > df["close"].iloc[-DIV_LOOKBACK] and rsi.iloc[highs_idx] < rsi.iloc[-DIV_LOOKBACK]:
        if rsi.iloc[highs_idx] >= RSI_HIGH:
            return "short", highs_idx
    return None, None

def compute_position_size(sl_usd):
    """Calcula cantidad de activo para arriesgar 1%"""
    risk_amount = ACCOUNT_USD * (RISK_PERCENT/100)
    qty = risk_amount / sl_usd
    return qty

# --- LOGICA BOT ---
for symbol in ASSETS:
    df_h1 = get_ohlc(symbol+"USDT", "1h", DIV_LOOKBACK+10)
    signal, idx_div = find_divergence(df_h1)
    if signal is None:
        continue  # sin trade

    # pasar a 5m para entrada
    df_5m = get_ohlc(symbol+"USDT", "5m", 50)
    ema = df_5m["close"].ewm(span=EMA_PERIOD).mean()
    # buscar vela que cierra con EMA dentro
    entry_price = None
    sl_price = None
    if signal == "long":
        sl_price = df_h1["low"].iloc[idx_div]
        for i in range(idx_div, len(df_5m)):
            if df_5m["close"].iloc[i] > ema.iloc[i-1] and df_5m["close"].iloc[i-1] < ema.iloc[i-1]:
                entry_price = df_5m["close"].iloc[i]
                break
    else:
        sl_price = df_h1["high"].iloc[idx_div]
        for i in range(idx_div, len(df_5m)):
            if df_5m["close"].iloc[i] < ema.iloc[i-1] and df_5m["close"].iloc[i-1] > ema.iloc[i-1]:
                entry_price = df_5m["close"].iloc[i]
                break
    if entry_price is None:
        continue

    # calcular TP escalonados
    R = abs(entry_price - sl_price)
    tps = [entry_price + R*r if signal=="long" else entry_price - R*r for r in SL_TP_RATIOS]

    trade = {
        "time": str(datetime.now()),
        "bot_id": "bot_v1",
        "activo": symbol,
        "signal": signal,
        "entry": entry_price,
        "sl": sl_price,
        "tp": tps,
        "qty": compute_position_size(R)
    }
    trades_data.append(trade)

# guardar trades
with open(FILE, "w") as f:
    json.dump(trades_data, f, indent=2)

print("Trades calculados y guardados."))
