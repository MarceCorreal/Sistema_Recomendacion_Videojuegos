from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq


app = FastAPI()


# Función Developer________________________________________________________________________________________________________________________________________________________________________________

def developer(df_developer, desarrollador):
    # Filtrar df por desarrollador
    
    df_developer_filtrado = df_developer[df_developer['developer'] == desarrollador]
    
    # Producir resultado
    
    respuestas_anuales  = df_developer_filtrado.groupby('release_year').agg({
        'items_free':'sum', 
        'items_total':'sum',
        'porcentaje': lambda x:(pd.to_numeric(x.str.rstrip('%'), errors='coerce') /  100).mean() *100
        }).reset_index()
    
    # Definir respuestas 
    respuestas_anuales['porcentaje'] = respuestas_anuales['porcentaje'].round(2)
    respuestas_anuales = respuestas_anuales.rename(columns={'release_year': 'Anio'})
    respuestas_anuales = respuestas_anuales.rename(columns={'items_total': 'Items'})
    respuestas_anuales = respuestas_anuales.rename(columns={'porcentaje': '%Free'})
    return respuestas_anuales[['Anio', 'Items', '%Free']]

# Definir ruta - Decorador_____________________________________________________________________________________________________________________________________

@app.get("/developer/{desarrollador}")

async def get_developer(desarrollador: str):

    
# Ejecución de la Función
    
    try:
        # Ruta_df_developer = r"C:\Users\Usuario\Henry\PI1_ML\Funciones\Developer\df_developer.parquet"
        ruta_df_developer = r"C:\Users\Usuario\Henry\PI1_MachineLearning\Funciones\Developer\df_developer.parquet"  #"Funciones/Developer/df_developer.parquet"
        df_developer = pd.read_parquet(ruta_df_developer)
        result = developer(df_developer, desarrollador)
        return result.to_dict(orient="records")
    except Exception as e:
        print(e)  # Imprimir el error para depuración
        return {'error': 'Ocurrió un error al procesar la solicitud'}
