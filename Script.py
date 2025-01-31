import subprocess
import re
import json
from datetime import datetime

#Ejecucion de la linea de comandos
def execute_conteo_command(command):
    try:
        # Ejecutar el comando SSH
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30
        )
        output = result.stdout

        # Verificar si hay errores en stderr
        if result.returncode != 0:
            Detalles = {
                "estatus": "CommandFailed",
                "comando" : command,
                "mensaje": result.stderr.strip(),
                "timestamp": datetime.now().isoformat(),
                "conteo" : None
            }
            return Detalles

        # Analizar la salida del ping
        Detalles = {
            "estatus": "Succsess",
            "comando" : command,
            "mensaje": 'Se completo la ejecucion de la setencia',
            "timestamp": datetime.now().isoformat(),
            "conteo": int(result.stdout.strip())
            }
        return Detalles

    except subprocess.TimeoutExpired:
        Detalles = {
            "estatus": "TimeoutExpired",
            "comando" : command,
            "mensaje": "El comando tardó demasiado en ejecutarse.",
            "timestamp": datetime.now().isoformat(),
            "conteo" : None
        }
        return Detalles
    
    except Exception as e:
        Detalles = {
            "estatus": "ExecutionError",
            "comando" : command,
            "message": str(e),
            "timestamp": datetime.now().isoformat(),
            "conteo" : None
        }         
        return Detalles

#################################################################################
# Ruta del archivo JSON
with open("Parametros.json", 'r') as archivo:
    Param = json.load(archivo)
Sentencias = Param['Parametros']['Sentencias']

# Creo un json para guardar los resultados
FormatLog = {
    "timeID": datetime.now().isoformat(),
    "service": "VALRISK.PP.OP.T03-S06-001-RAC001.Val-Datos-Integridad.RegitrosConAforoEnCero.v1.2.0",
    "level": "INFO",
    "resconteos": {}
}

# Cuento los archivos de todas las carpetas
flag = True
cnts = []
for key in Sentencias.keys():
    # Ejecutar el ping y capturar las métricas
    result = execute_conteo_command(Sentencias[key])
    FormatLog['resconteos'][key] = result
    
    # Reviso si hay alguna consulta fallida
    if result['estatus'] != 'Succsess':
        FormatLog['estatus'] = "Fail"
        FormatLog['mensaje'] =   "Hubo un fallo en el conteo de " + key
        flag = False
    else:
        cnts.append(result['conteo'])

# Reviso si todos los conteos se realizaron y si dan el mismo resultado
if flag == True:
    if len(set(cnts)) == 1:
        FormatLog['estatus'] = "Success"
        FormatLog['mensaje'] =  "Todas las carpetas tienen el mismo numero de archivos"
    else:
        FormatLog['estatus'] = "Diferencia"            
        FormatLog['diferencias'] = "Hay diferencia en el conteo de archivos de las carpetas"    
        
# Guardar en JSON
with open("Log.json", mode="w") as file:
    json.dump(FormatLog, file, indent=4)      