import json
import os
from datetime import datetime

FILE = "data.json"

BOT_ID = os.getenv("BOT_ID", "bot_v1")  # clave 🔥

if os.path.exists(FILE):
    with open(FILE, "r") as f:
        data = json.load(f)
else:
    data = []

registro = {
    "time": str(datetime.now()),
    "bot_id": BOT_ID,
    "activo": "BTC",
    "accion": "scan",
    "precio_fake": 65000
}

data.append(registro)

with open(FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"Guardado {BOT_ID}")
