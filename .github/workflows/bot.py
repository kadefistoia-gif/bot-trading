import json
import os
import random
from datetime import datetime

FILE = "data.json"

# cargar datos
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        data = json.load(f)
else:
    data = []

# generar tipo de evento
if random.random() < 0.3:
    tipo = "entry"
else:
    tipo = random.choice(["tp", "sl", "partial_tp"])

# registro nuevo
registro = {
    "time": str(datetime.now()),
    "bot_id": "bot_v1",
    "activo": "BTC",
    "evento": tipo,
    "precio": random.randint(60000, 70000),
    "cantidad": 1
}

data.append(registro)

with open(FILE, "w") as f:
    json.dump(data, f, indent=2)

print("Guardado OK:", tipo)
