
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


# developer_reviews_analysis________________________________________________________________________________________________________________________________________________________________________________

def developer_reviews_analysis(df, desarrolladora):

    '''
    Esta función realiza un análisis de sentimientos de las reseñas para una desarrolladora específica.
         
    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        desarrolladora (str): Nombre de la desarrolladora a analizar.
    
    Returns:
        dict: Un diccionario que contiene el resultado del análisis de sentimientos.
            - La clave es el nombre de la desarrolladora.
            - El valor es una lista con la cantidad de reseñas negativas y positivas.
    '''

    filtered_data = df[df['developer'] == desarrolladora]
    positive_count = 0
    negative_count = 0

    for sentiment in filtered_data['sentiment_analysis']:
        if sentiment == 0:
            negative_count += 1
        elif sentiment == 2:
            positive_count += 1

    result = {desarrolladora: [f"Negative = {negative_count}", f"Positive = {positive_count}"]}
    return result

@app.get("/developer_reviews_analysis/{desarrolladora}",
                    description=
                    """ <font color="black">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese el developer en el box abajo. Ejemplo: Valve <br>
                    3. Scrollear a "Response body" para ver cuantas reseñas positivas y negativas tuvo el desarrollador.
                    </font>"""
                    , tags=['Consultas PI1-ML'])
async def get_developer_reviews_analysis(desarrolladora: str):
    try:
        parquet_path5 = r"C:\Users\Usuario\Henry\PI1_ML\Funciones\developer_reviews_analysis\dataset_endpoint_5.parquet"
        #parquet_path5 = "C:\Users\Usuario\Henry\PI1_ML\Funciones\developer_reviews_analysis\dataset_endpoint_5.parquet"
        df = pd.read_parquet(parquet_path5)
        result = developer_reviews_analysis(df, desarrolladora)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



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
                    , tags=['Consultas PI1-ML'])
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

    
# Userforgenre________________________________________________________________________________________________________________________________________________________________________________

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
                    , tags=['Consultas PI1-ML'])
async def get_user_for_genre(genre: str):
    try:
        parquet_path3 = r"C:\Users\Usuario\Henry\PI1_ML\Funciones\userforgenre\dataset_endpoint_3.parquet"
        #parquet_path3 = "C:\Users\Usuario\Henry\PI1_ML\Funciones\userforgenre\dataset_endpoint_3.parquet"
        df = pd.read_parquet(parquet_path3)
        result = UserForGenre(genre, df)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



# best_developer_year________________________________________________________________________________________________________________________________________________________________________________

def best_developer_year(dataframe, year):

    '''
    Esta función devuelve los mejores desarrolladores para un año específico basado en el análisis de sentimientos.
         
    Args:
        dataframe (pd.DataFrame): DataFrame que contiene los datos.
        year (int): Año para el cual se desean obtener los mejores desarrolladores.
    
    Returns:
        list: Una lista de diccionarios que contiene información sobre los mejores desarrolladores.
            - Cada diccionario tiene la forma: {"Puesto [posición]: [nombre del desarrollador]": [sentimiento total]}
    '''

    df_year = dataframe[dataframe['release_anio'] == year]
    df_filtered = df_year[df_year['sentiment_analysis'] == 2]
    df_grouped = df_filtered.groupby('developer')['sentiment_analysis'].sum().reset_index()
    df_sorted = df_grouped.sort_values(by='sentiment_analysis', ascending=False)
    top_developers = df_sorted.head(3)
    result = [{"Puesto {}: {}".format(i+1, row['developer']): row['sentiment_analysis']} for i, (_, row) in enumerate(top_developers.iterrows())]
    return result

@app.get("/best_developer_year/{year}",
                    description=
                    """ <font color="black">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese un año para saber el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado.. Ejemplo: 2015 <br>
                    3. Scrollear a "Response body" para ver el resultado.
                    </font>"""
                    , tags=['Consultas PI1-ML'])
async def get_best_developer_year(year: int):
    try:
        parquet_path4 = r"Funciones\best_developer_year\dataset_endpoint_4.parquet"
        #parquet_path4 = "C:\Users\Usuario\Henry\PI1_ML\Funciones\best_developer_year\dataset_endpoint_4.parquet"
        df = pd.read_parquet(parquet_path4)
        result = best_developer_year(df, year)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    
    
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

@app.get("/developer/{desarrollador}",
                    description=
                    """ <font color="black">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese un desarrollador para ver la cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora. Ejemplo: Valve <br>
                    3. Scrollear a "Response body" para ver el resultado.
                    </font>"""
                    , tags=['Consultas PI1-ML'])
async def get_developer(desarrollador: str):
    try:
        #parquet_path = "C:\Users\Usuario\Henry\PI1_ML\Funciones\developer\dataset_endpoint_1.parquet"
        parquet_path = r"C:\Users\Usuario\Henry\PI1_ML\Funciones\developer\dataset_endpoint_1.parquet"
        df = pd.read_parquet(parquet_path)
        result = developer(df, desarrollador)
        return result.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")


