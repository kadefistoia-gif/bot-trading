import json
import os
from datetime import datetime

FILE = "data.json"

# cargar datos
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        data = json.load(f)
else:
    data = []

registro = {
    "time": str(datetime.now()),
    "bot_id": "bot_v1",
    "activo": "BTC",
    "accion": "scan",
    "precio_fake": 65000
}

data.append(registro)

with open(FILE, "w") as f:
    json.dump(data, f, indent=2)

print("Guardado OK")
