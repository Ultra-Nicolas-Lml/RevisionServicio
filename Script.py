import subprocess
import re
import json
from datetime import datetime

#Ejecucion de la linea de comandos
def execute_ping_command(command,FormatLog):
    try:
        # Ejecutar el comando SSH
        result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30
        )
        output = result.stdout.decode() if isinstance(result.stdout, bytes) else result.stdout

        # Verificar si hay errores en stderr
        if result.returncode != 0:
            Detalles = {
                "estatus": "CommandFailed",
                "mensaje": result.stderr.strip(),
                "timestamp": datetime.now().isoformat()
            }
            FormatLog['detalles'] = Detalles
            FormatLog['metricas'] = None
            return FormatLog

        # Analizar la salida del ping
        metrics = parse_ping_output(output)
        metrics["timestamp"] = datetime.now().isoformat()
        Detalles = {
            "estatus": "Succses",
            "mensaje": 'Se completo la ejecucion de la setencia',
            "timestamp": datetime.now().isoformat()}
        FormatLog['detalles'] = Detalles
        FormatLog['metricas'] = metrics
        return FormatLog

    except subprocess.TimeoutExpired:
        Detalles = {
            "estatus": "TimeoutExpired",
            "mensaje": "El comando tardó demasiado en ejecutarse.",
            "timestamp": datetime.now().isoformat()
        }
        FormatLog['detalles'] = Detalles
        FormatLog['metricas'] = None        
        return FormatLog
    
    except Exception as e:
        Detalles = {
            "estatus": "ExecutionError",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }
        FormatLog['detalles'] = Detalles
        FormatLog['metricas'] = None         
        return FormatLog

# Obtencion de metricas
def parse_ping_output(output):
    # Inicializar métricas
    metrics = {
        "packets_transmitted": 0,
        "packets_received": 0,
        "packet_loss": 0.0,
        "rtt_min": None,
        "rtt_avg": None,
        "rtt_max": None,
        "rtt_mdev": None
    }

    # Analizar líneas clave de la salida
    for line in output.splitlines():
        if "packets transmitted" in line:
            match = re.search(
                r"(\d+) packets transmitted, (\d+) received, (\d+)% packet loss", line
            )
            if match:
                metrics["packets_transmitted"] = int(match.group(1))
                metrics["packets_received"] = int(match.group(2))
                metrics["packet_loss"] = float(match.group(3))

        elif "rtt min/avg/max/mdev" in line:
            match = re.search(
                r"rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms", line
            )
            if match:
                metrics["rtt_min"] = float(match.group(1))
                metrics["rtt_avg"] = float(match.group(2))
                metrics["rtt_max"] = float(match.group(3))
                metrics["rtt_mdev"] = float(match.group(4))

    return metrics


# Ruta del archivo JSON
with open("Parametros.json", 'r') as archivo:
    Param = json.load(archivo)
Sentencias = Param['Parametros']['Sentencias']

# Creo un json para guardar los resultados
Resultados = {}
Resultados['Logs'] = []
LogTime = datetime.now().isoformat()


for sen in Sentencias:
    
    FormatLog = {
        "timeID": datetime.now().isoformat(),
        "service": "VALRISK.PP.OP.T03-S06-001-RAC001.Val-Datos-Integridad.RegitrosConAforoEnCero.v1.2.0",
        "sentencia": sen,
        "level": "INFO"
    }
    # Ejecutar el ping y capturar las métricas
    result = execute_ping_command(sen,FormatLog)
    Resultados['Logs'].append(result)
    
# Guardar en JSON
with open("Log.json", mode="w") as file:
    json.dump(Resultados, file, indent=4)      