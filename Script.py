import subprocess
from datetime import datetime
import json

# Ruta del archivo JSON
with open("Parametros.json", 'r') as archivo:
    Param = json.load(archivo)
servicios = Param['Parametros']['Hosts']

# Funcion que realiza la prueba ping
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
    
# Funcion que construye el log
def log_to_csv(host,status, time_ms):
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "service": "VALRISK.PP.OP.T03-S06-001-RAC001.Val-Datos-Integridad.RegitrosConAforoEnCero.v1.2.0",
        "host": host,
        "level": "INFO",
        "message": "Este es una prueba de lo que deberia de contener el mensaje",
        "transactionId": "1234567890",
        "detalles": 
            {
            "time": time_ms,
            "input": "<Entradas>",
            "output": status,
            "error": "<ErrorDetalles>"
            }
    }

    return data 

# Creo un json para guardar los resultados
Resultados = {}
Resultados['Logs'] = []

for servicio in servicios:
    status, time_ms = ping_ip(servicio)
    Resultados['Logs'].append(log_to_csv(servicio,status, time_ms))

# Guardar en JSON
with open("Log.json", mode="w") as file:
    json.dump(Resultados, file, indent=4)      