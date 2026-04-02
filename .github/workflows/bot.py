import json
import os
from datetime import datetime

# archivo donde guardamos datos
FILE = "data.json"

# cargar datos existentes
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        data = json.load(f)
else:
    data = []

# simulación de scan
registro = {
    "time": str(datetime.now()),
    "bot_id": "bot_v1",
    "activo": "BTC",
    "accion": "scan",
    "precio_fake": 65000
}

data.append(registro)

# guardar
with open(FILE, "w") as f:
    json.dump(data, f, indent=2)

print("Scan guardado:", registro)
