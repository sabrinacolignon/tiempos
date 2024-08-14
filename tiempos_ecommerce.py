import pandas as pd

def solapamientos(data: pd.DataFrame) -> (int, list): # type: ignore
    """Funcion para detectar solapaientos entre eventos en un DataFrame dado, utilizando una ventana de tiempo

    Parámetros:
    data (pd.DataFrame): DataFrame con los datos de los vuelos ya acondicionados y filtrados.

    Retorna:
    int: Cantidad de solapamientos encontrados.
    list: Lista de tuplas con los tiempos de los vuelos solapados.
    """
    solapamientos = 0
    t_solapados = []
    for i in range(len(data)):
        timestamp_i = data["Timestamp"].iloc[i]
        for j in range(i + 1, len(data)):
            timestamp_j = data["Timestamp"].iloc[j]
            
            # Si el siguiente timestamp está fuera de la ventana de solapamiento, rompe el bucle
            if timestamp_j > timestamp_i + pd.Timedelta(seconds = 1):
                break
            solapamientos += 1
            t_solapados.append((timestamp_i, timestamp_j))
    return solapamientos, t_solapados


# Abro el archivo y lo guardo en la variable data:
archivo = "./data/ecommerce.csv"

data = pd.read_csv(archivo, sep=",")

# Acondicionamiento:
data.dropna(inplace=True)

data["Timestamp"] = pd.to_datetime(data["Timestamp"])

# Ordeno por Timestamp
data.sort_values(by="Timestamp", inplace=True)
data.reset_index(drop=True, inplace=True)

#print(data["Timestamp"].head())

# Llamo a la función para detectar solapamientos:
cantidad_solapamientos, tiempos_solapados = solapamientos(data)

print("Cantidad de solapamientos: ", cantidad_solapamientos)
print("Tiempos solapados: ", tiempos_solapados)

# Calculo los solapamientos de tiempos con una ventana de 10 segundos:
enero = data[data["Timestamp"].dt.month == 1]
febrero = data[data["Timestamp"].dt.month == 2]
marzo = data[data["Timestamp"].dt.month == 3]
abril = data[data["Timestamp"].dt.month == 4]
mayo = data[data["Timestamp"].dt.month == 5]
junio = data[data["Timestamp"].dt.month == 6]

primer_t = pd.concat([enero, febrero, marzo, abril, mayo, junio], axis=0)

# Llamo a la función para detectar solapamientos:
cantidad_solapamientos_primer_t, tiempos_solapados_primer_t = solapamientos(primer_t)

print("Cantidad de solapamientos: ", cantidad_solapamientos_primer_t)
print("Tiempos solapados: ", tiempos_solapados_primer_t)