from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
import operator
import pyarrow as pa
import pyarrow.parquet as pq
from scipy.sparse import csr_matrix


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

    #if df_userdata_usuario.empty:
       # return f"El usuario {user_id} no existe en el DataFrame."

    # Obtener la primera fila
    
    dinero_gastado = usuario['cantidad total gastado'].iloc[0]
    porcentaje_recomendacion = float(usuario['percentage_true'].iloc[0].rstrip('%'))
    cantidad_items = usuario['item_id'].nunique()

    # Crear el diccionario de retorno
    
    resultado = {
        "Usuario": user_id,
        "Dinero gastado": f"${dinero_gastado:.2f} USD",
        "% de recomendación": f"{porcentaje_recomendacion:.2f}%",
        "Cantidad de items": cantidad_items
    }

    return resultado

# Definir ruta - Decorador userdata_____________________________________________________________________________________________________________________________________

@app.get("/userdata/{user_id}")

async def get_user_id(user_id: str):


    
# Ejecución de la Función developer
    
    try:
        parquet_path2 = r"C:\Users\Usuario\Henry\PI1_ML\Funciones\UserData\df_userdata.parquet"
        #parquet_path2  = "C:\Users\Usuario\Henry\PI1_ML\Funciones\UserData\df_userdata.parquet"
        df_userdata = pd.read_parquet(parquet_path2)
        result = userdata(df_userdata, user_id)
        return result.to_dict(orient="records")
    except Exception as e:
        print(e)  # Imprimir el error para depuración
        return {'error': 'Ocurrió un error al procesar la solicitud'}
