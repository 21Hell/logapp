import re
import pandas as pd
from datetime import datetime

# Ruta al archivo de log
LOG_FILE = 'password_log.txt'
# Ruta del archivo Excel de salida
EXCEL_FILE = 'resultado_fortaleza_contraseñas.xlsx'

# Función para verificar si una contraseña es fuerte
def es_contraseña_fuerte(password):
    return (len(password) >= 8 and
            re.search(r"[A-Z]", password) is not None and
            re.search(r"[a-z]", password) is not None and
            re.search(r"[0-9]", password) is not None and
            re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?/~\-]", password) is not None)

# Función para analizar el archivo de log y verificar la fortaleza de las nuevas contraseñas
def verificar_fortaleza_log():
    resultados = []  # Lista para almacenar los resultados

    with open(LOG_FILE, 'r') as log_file:
        for line in log_file:
            # Buscamos las líneas de log con contraseñas exitosas
            if "cambio de contraseña - éxito" in line:
                try:
                    # Extraemos la nueva contraseña usando regex
                    nueva_contraseña = re.search(r"Nueva contraseña: (\S+)", line).group(1)
                    
                    # Verificamos la fortaleza de la nueva contraseña
                    es_fuerte = es_contraseña_fuerte(nueva_contraseña)
                    estado = "fuerte" if es_fuerte else "débil"
                    
                    # Almacenamos los resultados en una lista
                    resultados.append({
                        "Fecha y hora": line.split(" - ")[0],
                        "Usuario": re.search(r"Usuario (\d+)", line).group(1),
                        "Contraseña antigua": re.search(r"Contraseña antigua: (\S+)", line).group(1),
                        "Nueva contraseña": nueva_contraseña,
                        "Fortaleza": estado
                    })
                except AttributeError:
                    # Si no encontramos una nueva contraseña en el formato esperado, omitimos la línea
                    print(f"No se pudo analizar la línea: {line.strip()}")

    # Guardamos los resultados en un archivo Excel
    if resultados:
        df = pd.DataFrame(resultados)
        df.to_excel(EXCEL_FILE, index=False)
        print(f"Los resultados se han guardado en {EXCEL_FILE}")
    else:
        print("No se encontraron resultados para guardar.")

# Ejecutamos la función
verificar_fortaleza_log()
