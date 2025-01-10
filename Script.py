import csv
import os
import subprocess
from datetime import datetime

servicio = 'pokeapi.co'
CSV_FILE = "Log.csv"

def ping_ip(servicio):
    try:
        # Realizar ping
        result = subprocess.run(["ping", "-c", "1", servicio], stdout=subprocess.PIPE, text=True, timeout=5)
        if result.returncode == 0:
            # Extraer el tiempo de respuesta
            for line in result.stdout.splitlines():
                if "time=" in line:
                    time_ms = line.split("time=")[-1].split(" ")[0]
                    return "Success", time_ms
        return "Failed", "N/A"
    except Exception as e:
        return "Error", str(e)
    
status, time_ms = ping_ip(servicio)

import json

def log_to_csv(status, time_ms):
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "service": "VALRISK.PP.OP.T03-S06-001-RAC001.Val-Datos-Integridad.RegitrosConAforoEnCero.v1.2.0",
        "level": "VALRISK.PP.OP.T03-S06-001-RAC001.Val-Datos-Integridad.RegitrosConAforoEnCero.v1.2.0",
        "message": "Este es una prueba de lo que deberia de contener el mensaje",
        "transactionId": "Transaccion",
        "detalles": 
            {
            "time": time_ms,
            "input": "<Entradas>",
            "output": status,
            "error": "<ErrorDetalles>"
            }
    }

    # Guardar en JSON
    with open("data.json", mode="w") as file:
        json.dump(data, file, indent=4)    

log_to_csv(status, time_ms)