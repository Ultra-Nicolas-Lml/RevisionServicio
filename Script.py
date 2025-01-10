import csv
import os
import subprocess
from datetime import datetime

servicio = 'pokeapi.co'
CSV_FILE = "/home/ubuntu/Scripts/Logs/Log.csv"

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

def log_to_csv(status, time_ms):
    # Crear archivo CSV si no existe
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "IP", "Status", "Response Time (ms)"])
        writer.writerow([datetime.now().isoformat(), servicio, status, time_ms])

log_to_csv(status, time_ms)