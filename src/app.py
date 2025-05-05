import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import urllib.request
from dotenv import load_dotenv

#Agregamos la URL en una variable
url = 'https://en.wikipedia.org/wiki/List_of_most-streamed_songs_on_Spotify'

# Realiza la solicitud http
response = requests.get(url)

#Solicitud para verificar el estado de la anterior solicitud HTTP
response.status_code

# Verificamos si la solicitud fue exitosa
if response.status_code==200:
   
    #Usamos esta funcion que lee todas etiquetas <table> de URL y convierte esas tablas en dataframes
    # devolviendo una lista de esos dataframes
    tables = pd.read_html(url)
    
    #Generar el dataframe df_canciones a partir de la primera tabla existente en la URL
    df_canciones = tables[0]
    #print(df_canciones.head())

else:
    print(f"Ocurrió un error: {response.status_code}")

# Eliminamos la columna ref ya que no tiene utilidad en nuestro contexto como parte del proceso de limpieza
# no encuentro valores nulos ni vacios en la tabla asi que no elimino nada mas
canciones_stremadas = df_canciones.drop(columns="Ref.")
#print(canciones_stremadas.head())

# Cargar variables de entorno
load_dotenv(override=True)
db_path = os.getenv("DB_PATH")

#print(db_path)

# Conectarse a la base de datos y guardar el DataFrame
conn = sqlite3.connect(db_path)
canciones_stremadas.to_sql("canciones", conn, if_exists="replace", index=False)
conn.close()

# Hacemos consulta de la tabla canciones
conn = sqlite3.connect(db_path)
df2 = pd.read_sql("SELECT * FROM canciones", conn)
print(df2)
conn.close()