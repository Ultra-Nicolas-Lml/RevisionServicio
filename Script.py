import subprocess
import json
from datetime import datetime

def compare_folders(command):
    try:
        # Ejecuta el comando diff
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30
        )
        output = result.stdout.strip()  # Elimina espacios innecesarios
        error_output = result.stderr.strip()  # Captura errores si los hay

        # Verificar si hay errores en stderr que indiquen fallo real
        if result.returncode != 0 and error_output:
            Detalles = {
                "estatus": "CommandFailed",
                "command": command,
                "mensaje": error_output,
                "timestamp": datetime.now().isoformat()
            }
            Detalles['diferencias'] = None
            return Detalles

        # Si `returncode == 1` pero no hay error en stderr, significa que hay diferencias
        Detalles = {
            "estatus": "Success",
            "command": command,
            "mensaje": "Ejecución completada correctamente.",
            "timestamp": datetime.now().isoformat()
        }
        Detalles['diferencias'] = output.splitlines() if output else []
        return Detalles

    except subprocess.TimeoutExpired:
        Detalles = {
            "estatus": "TimeoutExpired",
            "command": command,
            "mensaje": "El comando tardó demasiado en ejecutarse.",
            "timestamp": datetime.now().isoformat()
        }
        Detalles['diferencias'] = None        
        return Detalles
    
    except Exception as e:
        Detalles = {
            "estatus": "ExecutionError",
            "command": command,
            "mensaje": str(e),
            "timestamp": datetime.now().isoformat()
        }
        Detalles['diferencias'] = None        
        return Detalles

############################################################################################################3
# Ruta del archivo JSON
with open("Parametros.json", 'r') as archivo:
    Param = json.load(archivo)
BeginCommand = Param['Parametros']['BeginCommand']
Carpetas = Param['Parametros']['Carpetas']

CombCarp = []
for i in range(len(Carpetas)):
    for j in range(i+1,(len(Carpetas))):
        CombCarp.append(Carpetas[i]+" "+Carpetas[j])

# Creo un json para guardar los resultados
FormatLog = {
    "timeID": datetime.now().isoformat(),
    "service": "VALRISK.PP.OP.T03-S06-001-RAC001.Val-Datos-Integridad.RegitrosConAforoEnCero.v1.2.0",
    "level": "INFO",
    "resdiffs": {}
}

for comb in CombCarp:
    resultado = compare_folders(BeginCommand + " " + comb)
    FormatLog["resdiffs"][comb] = resultado
    
with open("resultado.json", "w") as archivo:
    json.dump(FormatLog, archivo, indent=4)