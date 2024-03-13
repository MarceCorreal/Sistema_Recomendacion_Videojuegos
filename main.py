# Importaciones de bibliotecas necesarias

from fastapi import FastAPI
import pandas as pd  # Pandas para manipulación de datos tabulares
import json  # Módulo para trabajar con JSON
import ast  # Módulo para evaluar expresiones literales de Python
import re  # Módulo para trabajar con expresiones regulares
from textblob import TextBlob # Importa la clase TextBlob desde la biblioteca TextBlob
import nltk # Importa la biblioteca nltk (Natural Language Toolkit)
import csv # Importa el módulo csv en Python

# Habilita la recarga automática de módulos antes de ejecutar una celda
#%load_ext autoreload
#%autoreload 2

# Importa el módulo de advertencias y configura para ignorar todas las advertencias
#import warnings
#warnings.filterwarnings("ignore")

# Importa el módulo de advertencias y configura para ignorar todas las advertencias
#import warnings
#warnings.filterwarnings("ignore")


app = FastAPI()


# Función Developer________________________________________________________________________________________________________________________________________________________________________________

def developer(df_developer, desarrollador):
    # Filtrar df por desarrollador developer
    
    df_developer_filtrado = df_developer[df_developer['developer'] == desarrollador]
    
    # Producir resultado developer
    
    respuestas_anuales  = df_developer_filtrado.groupby('release_year').agg({
        'items_free':'sum', 
        'items_total':'sum',
        'porcentaje': lambda x:(pd.to_numeric(x.str.rstrip('%'), errors='coerce') /  100).mean() *100
        }).reset_index()
    
    # Definir respuestas developer
    respuestas_anuales['porcentaje'] = respuestas_anuales['porcentaje'].round(2)
    respuestas_anuales = respuestas_anuales.rename(columns={'release_year': 'Anio'})
    respuestas_anuales = respuestas_anuales.rename(columns={'items_total': 'Items'})
    respuestas_anuales = respuestas_anuales.rename(columns={'porcentaje': '%Free'})
    return respuestas_anuales[['Anio', 'Items', '%Free']]

# Definir ruta - Decorador_____________________________________________________________________________________________________________________________________

@app.get("/developer/{desarrollador}")

async def get_developer(desarrollador: str):

    
# Ejecución de la Función developer
    
    try:
        # Ruta_df_developer = r"C:\Users\Usuario\Henry\PI1_ML\Funciones\Developer\df_developer.parquet"
        ruta_df_developer = r"C:\Users\Usuario\Henry\PI1_MachineLearning\Funciones\Developer\df_developer.parquet"  #"Funciones/Developer/df_developer.parquet"
        df_developer = pd.read_parquet(ruta_df_developer)
        result = developer(df_developer, desarrollador)
        return result.to_dict(orient="records")
    except Exception as e:
        print(e)  # Imprimir el error para depuración
        return {'error': 'Ocurrió un error al procesar la solicitud'}


# Función Userdata________________________________________________________________________________________________________________________________________________________________________________
def userdata(df_userdata, user_id):
    # Filtrar el DataFrame para obtener la información del usuario
    df_userdata_usuario = df_userdata[df_userdata['user_id'] == user_id]

    if df_userdata_usuario.empty:
        return f"El usuario {user_id} no existe en el DataFrame."

    # Obtener la primera fila
    
    dinero_gastado = df_userdata_usuario['cantidad total gastado'].iloc[0]
    porcentaje_recomendacion = float(df_userdata_usuario['percentage_true'].iloc[0].rstrip('%'))
    cantidad_items = df_userdata_usuario['item_id'].nunique()

    # Crear el diccionario de retorno
    
    resultado = {
        "Usuario": user_id,
        "Dinero gastado": f"${dinero_gastado:.2f} USD",
        "porcentaje de recomendación": f"{porcentaje_recomendacion:.2f}%",
        "Cantidad de items": cantidad_items
    }

    return resultado

# Definir ruta - Decorador userdata____________________________________________________________________________________________________________________________________

@app.get("/userdata/{user_id}")

async def get_userdata(user_id: str):

    
# Ejecución de la Función developer
    
    try:
        # Ruta_df_userdata = r"C:\Users\Usuario\Henry\PI1_ML\Funciones\UserData\df_userdata.parquet"
        ruta_df_userdata = r"C:\Users\Usuario\Henry\PI1_ML\Funciones\UserData\df_userdata.parquet"  
        df_userdata = pd.read_parquet(ruta_df_userdata)
        result = userdata(df_userdata, user_id)
        return result.to_dict(orient="records")
    except Exception as e:
        print(e)  # Imprimir el error para depuración
        return {'error': 'Ocurrió un error al procesar la solicitud'}

