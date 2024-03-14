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


# Developer________________________________________________________________________________________________________________________________________________________________________________
    
def developer(dataframe, desarrollador):

    '''
    Esta función devuelve estadísticas por año para un desarrollador específico en un DataFrame.
        
    Args:
        dataframe (pd.DataFrame): DataFrame que contiene los datos.
        desarrollador (str): Nombre del desarrollador a analizar.
    
    Returns:
        pd.DataFrame: Un DataFrame que contiene estadísticas por año para el desarrollador.
            - 'Año' (int): Año de lanzamiento.
            - 'Items' (int): Cantidad total de items lanzados por el desarrollador.
            - '% Free' (float): Porcentaje medio de items gratuitos lanzados por el desarrollador.
    '''

    df_desarrollador = dataframe[dataframe['developer'] == desarrollador]
    stats_por_anio = df_desarrollador.groupby('release_anio').agg({
        'items_free': 'sum',
        'items_total': 'sum',
        'percentage_free': lambda x: (pd.to_numeric(x.str.rstrip('%'), errors='coerce') / 100).mean() * 100
    }).reset_index()
    stats_por_anio['percentage_free'] = stats_por_anio['percentage_free'].round(2)
    stats_por_anio = stats_por_anio.rename(columns={'release_anio': 'Año'})
    stats_por_anio = stats_por_anio.rename(columns={'items_total': 'Items'})
    stats_por_anio = stats_por_anio.rename(columns={'percentage_free': '% Free'})
    return stats_por_anio[['Año', 'Items', '% Free']]

@app.get("/developer/{desarrollador}")

async def get_developer(desarrollador: str):
    try:
        #parquet_path = "C:\Users\Usuario\Henry\Nuevo_proyecto\Funciones\developer\dataset_endpoint_1.parquet"
        parquet_path = r"C:\Users\Usuario\Henry\Nuevo_proyecto\Funciones\developer\dataset_endpoint_1.parquet"
        df = pd.read_parquet(parquet_path)
        result = developer(df, desarrollador)
        return result.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")


@app.get("/developer/{desarrollador}")
async def get_desarrollador(desarrollador: str):
    try:
        parquet_path1 = "dataset_endpoint_1.parquet"
        #parquet_path1 =  "C:\Users\Usuario\Henry\Nuevo_proyecto\Funciones\developer\dataset_endpoint_1.parquet"
        
        df = pd.read_parquet(parquet_path1)
        
        # Llama a la función userdata
        result = userdata(df, desarrllador)
        return JSONResponse(content=result)
    except Exception as e:
        print(e)  # Imprimir el error para depuración
        return {'error': 'Ocurrió un error al procesar la solicitud'}
    
    
    
# Userdata________________________________________________________________________________________________________________________________________________________________________________

def userdata(df, user_id):

    '''
    Esta función devuelve información sobre un usuario según su 'user_id'.
         
    Args:
        df (pd.DataFrame): DataFrame que contiene los datos del usuario.
        user_id (str): Identificador único del usuario.
    
    Returns:
        dict: Un diccionario que contiene información sobre el usuario.
            - 'Usuario' (str): Identificador único del usuario.
            - 'Dinero gastado' (str): Cantidad de dinero gastado por el usuario en formato USD.
            - '% de recomendación' (str): Porcentaje de recomendaciones realizadas por el usuario.
            - 'Cantidad de items' (int): Cantidad de items únicos que tiene el usuario.
    '''

    usuario = df[df['user_id'] == user_id]

    if usuario.empty:
        raise HTTPException(status_code=404, detail=f"El usuario {user_id} no existe en el DataFrame.")

    dinero_gastado = usuario['cantidad total gastado'].iloc[0]
    porcentaje_recomendacion = float(usuario['percentage_true'].iloc[0].rstrip('%'))
    cantidad_items = usuario['item_id'].nunique()

    resultado = {
        "Usuario": user_id,
        "Dinero gastado": f"${dinero_gastado:.2f} USD",
        "% de recomendación": f"{porcentaje_recomendacion:.2f}%",
        "Cantidad de items": cantidad_items
    }

    return resultado

@app.get("/userdata/{user_id}",
                    description=
                    """ <font color="black">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese un identificador de usuario (user_id) para Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.. Ejemplo: GamekungX <br>
                    3. Scrollear a "Response body" para ver el resultado.
                    </font>"""
                    , tags=['Consultas generales'])
async def get_user_id(user_id: str):
    try:
        parquet_path2 = "Dataset/dataset_endpoint_2.parquet"
        #parquet_path2 = "C:/Users/Usuario/Desktop/Repositorios Github/HENRY_Proyecto_Individual_1_MLOps_Orestes_Victor/Dataset/dataset_endpoint_2.parquet"
        # Lee el DataFrame desde el archivo Parquet
        df = pd.read_parquet(parquet_path2)
        
        # Llama a la función userdata
        result = userdata(df, user_id)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    
#3° Endpoint________________________________________________________________________________________________________________________________________________________________________________

def UserForGenre(genre: str, df):

    '''
    Esta función devuelve información sobre el usuario con más horas jugadas para un género específico.
         
    Args:
        genre (str): Género para el cual se desea obtener la información.
        df (pd.DataFrame): DataFrame que contiene los datos.
    
    Returns:
        dict: Un diccionario que contiene información sobre el usuario con más horas jugadas para el género.
            - 'Usuario con más horas jugadas para género [genre]' (str): Identificador del usuario con más horas jugadas.
            - 'Horas jugadas' (list): Lista de diccionarios con el año y las horas jugadas por año.
                - 'Año' (int): Año de lanzamiento.
                - 'Horas' (int): Horas jugadas por año.
    '''

    df['release_anio'] = pd.to_numeric(df['release_anio'], errors='coerce', downcast='integer')
    genre_df = df[df['genres'] == genre]
    genre_df['playtime_forever'] = (genre_df['playtime_forever'] / 60 / 60).astype(int)
    max_playtime_user = genre_df.loc[genre_df['playtime_forever'].idxmax(), 'user_id']
    yearly_playtime = genre_df.groupby('release_anio')['playtime_forever'].sum().reset_index()
    playtime_list = [{'Año': int(year), 'Horas': int(hours)} for year, hours in zip(yearly_playtime['release_anio'], yearly_playtime['playtime_forever'])]
    result = {"Usuario con más horas jugadas para género " + genre: max_playtime_user, "Horas jugadas": playtime_list}
    return result

@app.get("/user_for_genre/{genre}",
                    description=
                    """ <font color="black">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese un genero para devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento. Ejemplo: Action <br>
                    3. Scrollear a "Response body" para ver el resultado.
                    </font>"""
                    , tags=['Consultas generales'])
async def get_user_for_genre(genre: str):
    try:
        parquet_path3 = r"C:\Users\Usuario\Henry\PI1_ML\Funciones\userforgenre\dataset_endpoint_3.parquet"
        #parquet_path3 = "C:\Users\Usuario\Henry\PI1_ML\Funciones\userforgenre\dataset_endpoint_3.parquet"
        df = pd.read_parquet(parquet_path3)
        result = UserForGenre(genre, df)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)




