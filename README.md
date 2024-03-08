<p align="center">
<img src="https://github.com/MarceCorreal/PI1_ML/blob/main/Assets/logo_steam%20(1).svg" />
</p>

<h1 align="center"><b>PROYECTO INDIVIDUAL 1 - MACHINE LEARNING - DPT07</b></h1>

<h1 align="center"><b>Sistemas de Recomendación de Videojuegos para usuarios plataforma STEAM</b></h1>

## Autor: Marcela Correal García

## Generalidades del Repositorio

<p style="text-align: justify;">

El presente proyecto se presenta como requisito para aprobar el módulo de laboratorios de Henry

Consiste en desarrollar un sistema de recomendación de videojuegos de la tienda Steam, surtiendo todos los pasos que se deben tener en cuenta para esta misión.

El proyecto se desarrolla en VPython - VisualCode Studio

El repositorio de Henry con las consignas se encentran en: https://github.com/soyHenry/PI_ML_OPS/blob/FT/Readme.md

</p>


## Objetivo del Proyecto 

El objetivo del proyecto es desarrollar un flujo de trabajo eficiente que incluya la recopilación y transformación de datos, el  análisis exploratorio, el desarrollo de un mmodelo de machine learning y su implementación.

Este proyecto tiene como objetivo, desarrollar un Producto Mínimo Viable que incluya una API en la nube y la implementación de dos modelos de Machine Learning: análisis de sentimientos en comentarios de usuarios y recomendación de juegos basada en nombre o preferencias de usuario.

## Flujo de Trabajo

- EDA & ETL
- Desarrollo ML-OPS
- Implementación ML-OPS
- Presentación


### EDA & ETL

Se recibieron 3 carpetas,a cada uno se le hizo un EDA y ETL paralelamente, pues entender los datos y transformarlos paralelamente es más eficiente. como evidencia de este etapa quedan en el repositorio 1 notebook de EDA  y 1 dataframe en parquet por cada carpeta recibida.

Loas 3 archivos EDAS, iniciaron con la importación de las siguientes bibliotecas:

- Pandas (import pandas as pd): Con el fin de trabajar los datos, por su volumen
- JSON (import json): Dado que los archivos al descomprimires estan en formato Json
- Expresiones Regulares (import re) para coincidir las busquedas con cadenas de texto
 -AST (import ast): Est biblioteca fué necesario descargarla ya que los dataset tenían una estructura abstracta 
- TextBlob: proporciona herramientas para el procesamiento de lenguaje natural (NLP)


A continuación, se presenta un apartado de cada uno de las carpetas recibidas con los comentarios particulares de esta etapa, aunque los pasos operativos se encuentran en los comentarios del mismo notebook en Jupyter:

* __Steam_Games__: Se revisa una carpeta comprimida .gz que contiene un archivo json.
  Al abrir este archivo en plano, parece ser un diccionario pues tiene formato clave valor de 13 columnas. continene un archivo llamado output_steam_games
  La información se refiere a las características del juego como tal
  Lo primero es descomprimirlo, abrirlo y convertir los datos en un dataframe de pandas y se observa lo siguiente:
    
  Tipo: diccionario
  
  Size: 120.445 x 13 despues de eliminan NAN 22.530
  
  Tamaño: 113 MB
  
  EL Dataframe tiene columnas anidadas, es decir listas dentro de listas que se deben desanidar
  
  Se ven columnas repetidas como genres y tags, como app_name y title, se debe borrar una de ellas
  
  Se deben tener en cuenta el tipo de datos en que viene cada columna: todos en object y id y early acces en Float64. en caso que early acces se refiera a una fecha tocará cambiarle el tió
  Para desanida se utilizó función explode que aumenta el numero de filas repitiendo las columnas

    
 * __User_Reviews__: Inicialmente se revisan las características de los datos en plano y se puede observar que el archivo Json que incluye la carpeta se llama australian_user_reviews
   Tambien parece contener un diccionario pues inicia con corchetes y tiene : lo que indica que incluye claves.
   Lo primero es descomprimir el archivo de la misma forma que se hizo con el anterior.
  
   En este caso lo que se hizo fué desarrollar una fórmula para que leyera los archivos que son cadenas en este caso y recorrerlos par apasar los datos a la lista que se creo. 
   También se utilizó la función ast_literal
   
   al abrirlo en Pandas verifico que es un dataframe con 3 columnas referente al usuario, el id, la url y los reviews que hay que explodar por que e ve que vienen anidadas.
   
   Como en los otros casos, los pasos operativos, se encuentran explicados el detalle en el notebook.
   Para desanidar la ultima columna se utilizó explide y normalize que independiza la columna y eso hace que se puede volver a desanidar
   
   Posteriormente, se reindexa la columna explode y se vuelven a juntar mediante un merge para tener un solo dataframe final con toda la información 
   
   En este momento, cambio el nombre del archivo por df_user_reviews_sentimiento, dado que incluiré una columna de sentimiento tal como indica la consigna.
   
   Este data frame cuenta con las siguientes características:

    Tipo: diccionario
    
    Size: 25798x3 antes de desanidar
    
    Tamaño: 1.8+ MB
  
    En el dataset user_reviews se incluyen reseñas de juegos hechos por distintos usuarios. Debes crear la columna 'sentiment_analysis' 
    aplicando análisis de sentimiento con NLP con la siguiente escala: debe tomar el valor '0' si es malo, '1' si es neutral 
    y '2' si es positivo. Esta nueva columna debe reemplazar la de user_reviews.review para facilitar el trabajo de los modelos 
    de machine learning y el análisis de datos. De no ser posible este análisis por estar ausente la reseña escrita, debe tomar el valor de 1
    
    Para lo anterior se plició  df['Sentimiento'] = df['Texto'].apply(analizar_sentimiento)

 * __Users_Items__: Esta carpeta comprimida incluye un archivo llamado australian_users_items.
   También en codificación UTF-8
   
     Este data frame cuenta con las siguientes características:
  
    Tipo: diccionario
    
    Size: 441.550 x 5 
    
    Tamaño: 3.4 MB
  
    En este caso, después de descomprimir tambien fué necesario crear una lista y recorrer la información para llanearla, espte proceso se tomó mucho tiempo por el tamaño
    
    LA información esta en 5 columnas referente a la información de los usuarios y sus referencias.
    La quinta columna se debe desanidar con eol mismo procedimiento: explode, normalize, indexar y merge


### Desarrollo ML-OPS

Ejemplos adicionales de cómo usar el proyecto en diferentes situaciones o escenarios.

### Implementación ML-OPS

Información sobre cómo contribuir al proyecto, incluyendo pautas de contribución y cómo enviar solicitudes de extracción.

### Presentación

Reconocimiento a cualquier persona, proyecto o recurso externo que haya sido utilizado en la creación del proyecto


## Documentación
<p style="text-align: justify;">

En el Presente repositorio se encontrarán los notebooks de Jupyter en que se trabajan los datos y la programación del proyecto. 

Los documentos y data sets para la entrega se encontrarán además, en el siguiente Drive de Google creado para este fin:

[[https://drive.google.com/drive/folders/1npceA-nxhnUVxT3Y0qtKvKYyVYIIaaGL?usp=sharing](https://drive.google.com/drive/folders/13gMlg5p4hE9f6q6UP05ZRnvu3DlLbGvg?usp=drive_link)]

</p>



## Pasos para el desarrollo del Proyecto

1 - 


La primera parte del proyecto es desarrollar el EDA de los archivos recibidos en la consigna donde se entienden los datos que se entregan en la consigna y el ETL donde será necesario efectuar las transformaciones mínimas de cada archivo recibido.

1- EDA
A cada uno de los archivos comprimidos Json.gz se le desarrolló un estudio para saber la información que contenía. En general, la data se encontraba cruda por lo que fué necesario, en primera instancia en cada uno de los archivo, borrar, los nulos y los vación con drop.na Posteriormente, se eliminarion los registros duplicados con .drop_duplicates()

Algunos registos se veían anidados en listas de diccionarios, pr lo tanto el primer tratamiento para esos casos fué utilizar el método explode, lo que desanida en un primer nivel ese tipo de registros y posteriormente se normalizaban las columnas lo que independizaba la columna de los diccionario y aplana el archivo. Cuando el data frame se encuentra desanidado, basta con indexar los data fames explotados y normalizados para utilizar el concat y reunir toda la información en un mismo data frame. De igual forma, fué necesario borrar las columas que no agregaban valor, que no se borraron todas, pues pensé que depronto se necesaitarían a futuro para alguna función

Relaciones: Las relaciones principales que se encontro entre los tres data frame fueron las siguientes:

App_name de SteamGames contenia la misma información que item_name en users_items y se refiere el nombre. Por esto cambié el nomre de item_name
user_id en users_reviews y user_id en users items es el mismo
Para asegurarme de las relaciones que veia a simple vista organice los data frames de menor a mayor por la columna que estaba revisando df_organizado = df.sort_values(by='nombre_columna')
2- Funciones
Antes de desarrollar las APIS, tomé la desición de desarrollar las funciones en local

El análisis y desarrollo para el desarrollo de las funciones es el siguiente:

def fx_developer( desarrollador : str ): Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.
Ejemplo de retorno: Año Cantidad de Items Contenido Free 2023 50 27% 2022 45 25% xxxx xx xx%

Para Esta función se utilizan los siguientes datos: Release year que se encuentra en steam games, price que tambien está en steam games y el desarrollador que tambien lo está

Es decrir que para el dataframe de esta función df_developer, solo necesito modificar steam games

Primero hago un dataframe con solo la info que se necesita partiendo de steam games que es donde esta toda la información

Luego agrupar por developer, filtrar por año, contar el total de los items y contar los items donde el precio es = 0

Y con esta información encontrar el porcentaje final.

def userdata( User_id : str ): Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.
Ejemplo de retorno: {"Usuario X" : us213ndjss09sdf, "Dinero gastado": 200 USD, "% de recomendación": 20%, "cantidad de items": 5}

def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.
Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

def best_developer_year( año : int ): Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

¨def developer_reviews_analysis( desarrolladora : str ): Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.

Ejemplo de retorno: {'Valve' : [Negative = 182, Positive = 278]}

Dirección del Render https://pi1-machinelearning.onrender.com












