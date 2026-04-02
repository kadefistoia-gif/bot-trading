import streamlit as st
import json
from datetime import datetime, timedelta
from config import ASSETS

DATA_FILE = "data.json"

st.set_page_config(page_title="Trading Bot Dashboard", layout="wide")
st.title("📊 Bot Trading Dashboard")

# --- Cargar datos ---
try:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
except:
    data = []

# Separar trades y watchlist
trades = []
watchlist = []

for d in data:
    if "entry" in d:  # trade confirmado
        trades.append(d)
    elif "signal" in d and "entry" in d and d.get("status", "watching") == "watching":
        watchlist.append(d)

# --- Último scan ---
if data:
    last_scan = max(datetime.fromisoformat(d["time"]) for d in data)
    next_scan = last_scan + timedelta(minutes=5)
else:
    last_scan = None
    next_scan = None

st.markdown(f"**Último scan:** {last_scan}")
st.markdown(f"**Próximo scan estimado:** {next_scan}")

# --- Tabla de trades ---
st.subheader("📈 Trades realizados")
if trades:
    st.table(trades)
else:
    st.write("No hay trades registrados aún.")

# --- Watchlist ---
st.subheader("👀 Watchlist (pendientes de entrada limit)")
if watchlist:
    # Mostrar tiempo en vigilancia
    for w in watchlist:
        w["time_in_watch"] = str(datetime.now() - datetime.fromisoformat(w["time"]))
    st.table(watchlist)
else:
    st.write("No hay activos en vigilancia.")

# Botón de refrescar
if st.button("🔄 Refrescar"):
    st.experimental_rerun()
