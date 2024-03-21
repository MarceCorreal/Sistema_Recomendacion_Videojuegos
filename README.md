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

El objetivo del proyecto es desarrollar un flujo de trabajo eficiente que incluya la recopilación y transformación de datos, el  análisis exploratorio, el desarrollo de un modelo de machine learning y su implementación.

Este proyecto tiene como objetivo, desarrollar un Producto Mínimo Viable que incluya una API en la nube y la implementación de dos modelos de Machine Learning: análisis de sentimientos en comentarios de usuarios y recomendación de juegos basada en nombre o preferencias de usuario.

## Documentación
<p style="text-align: justify;">

En el Presente repositorio se encontrarán los notebooks de Jupyter en que se trabajan los datos y la programación del proyecto. 

Los documentos y data sets para la entrega se encontrarán además, en el siguiente Drive de Google creado para este fin:

(https://drive.google.com/drive/folders/1CqnqcrPWDIGo0FuxSTAd9qHw1pqiysAq?usp=drive_link)

</p>



## Flujo de Trabajo

- EDA & ETL
- Desarrollo ML_OPS 
- Modelo ML
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

* Steam_Games: Se revisa una carpeta comprimida .gz que contiene un archivo json.
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

 El archivo descrito se encuentra en el siguiente vínculo:

 (https://drive.google.com/file/d/1vcobbjAteXjgmQ0_Vh8YwkDtLE2YEO3d/view?usp=drive_link)

    
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

   (https://drive.google.com/file/d/1QByUDCu5Wz7uzEfh1KFgFIBVZZYOFqnV/view?usp=sharing)

 * __Users_Items__: Esta carpeta comprimida incluye un archivo llamado australian_users_items.
   También en codificación UTF-8
   
     Este data frame cuenta con las siguientes características:
  
    Tipo: diccionario
    
    Size: 441.550 x 5 
    
    Tamaño: 3.4 MB
  
    En este caso, después de descomprimir tambien fué necesario crear una lista y recorrer la información para llanearla, espte proceso se tomó mucho tiempo por el tamaño
    
    LA información esta en 5 columnas referente a la información de los usuarios y sus referencias.
    La quinta columna se debe desanidar con eol mismo procedimiento: explode, normalize, indexar y merge

(https://drive.google.com/file/d/1vgdqcwLVbi3HtMI8AuaECHh_LCM0b6BA/view?usp=sharing)
   ## Desarrollo ML_OPS 
   ## Funciones
   

   Cada una de las funciones a continuación cuenta con una carpeta individual en el github, deon de se encontraá un archivo del desarrollo del daraframe de la función, el datframe de la función y un notebook de la función

   Todas las funciones se ven desarrolladas en el main por lo que no hace falta adjuntarlas

   # def developer( *`desarrollador` : str* ):
    
     Devuelve la`Cantidad` de items y `porcentaje` de contenido Free por año según empresa desarrolladora.
   
    # def **userdata( *`useridr` : str* )**:
    
    Devuelva la  cantidad de dinero gastado por el usuario que ingresa el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.
    
    # def UserForGenre( genero : str ):

    Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

   # def best_developer_year( año : int ):

    Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)

   # def developer_reviews_analysis( desarrolladora :

    Devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.

Posterior a la elaboración de las funciones, con ayuda de Fast API y render, se desplegaron las funciones anteriormente descritas en aplicaciones para servirse el en el servidor 
SWAGGER - local host http://127.0.0.1:8000/docs

Inicialmente, después de desarrollar los data frame individuales para cada función y desarrollar cada función en local,
se probó cada una de las funciones con algún ejemplo para verificar su correcto funcionamiento.

Cada una de las funciones cuenta con una carpeta donde se aloja el df de la función, la función en local  y el archivo en jupiter 
donde se dasarrolló cada una de los dataframes de cada función-

Posteriormente se desarrollo el archivo main alojado en la carpeta raiz del proyecto, en la que, después de importar todas las 
bibliotecas necesarias para todas las funciónes, se instanció la aplicación fast api:

app = FastAPI()

A renglón seguido se deja en espacio para cada función, en la que se escriben las instrucciones para el usuario y se provee un 
ejemplo para su utilización.

En el espacio de cada función, se copia la función ya probada y se indica lo siguiente:

@app.get("/developer_reviews_analysis/{desarrolladora}",
async def get_developer_reviews_analysis(desarrolladora: str):

incluyendo el nombre de la función y el argumento que ingresará el usuario dentro de corchetes.
Se utilizó el método get para todas las funciones y se dejó un sólo tag llamado 'Consultas PI1-ML' 
para indicar la finalidad de las funciones.

Despés de verificar que cada una de las funciones corría de forma indicada sin bugs en visual,
Se pasó a levantar render generando la conexión desde la página de render siguiento las indicaciones
con mi repositorio en github.

### Modelo de Aprendizaje Automático

Con el fin de organizar la información del proyecto, se creó en el repositorio una carpeta llemada Modelo_Aprendizaje automático
Para desarrollar este aparte, se debe iniciar por el análisis de toda la base de datos para encontrar juegos similares al juego 
proporcionado por el usuario activo. 
El algoritmo trata de identificar la similitud entre los juegos al utilizar la similitud del coseno que sugiere la consigna, como medida.
La similitud del coseno es una técnica comúnmente empleada en sistemas de recomendación y análisis de datos para evaluar cuán similares
son dos conjuntos de datos o elementos

El desarrollo del coseno  proporciona una medida cuantitativa de la similitud entre juegos, permitiendo al modelo generar recomendaciones 
basadas en juegos que comparten características similares.

Con el fin de  organizar la organización para el desarrollo del modelo se crean las siguientes carpetas:

* Datos_Modelos_ en la que se van a manipular, analizar los datos y dejarlos en data frame facil de manejar en pandas por temas de espacio
* Modelo_Recomendación con el modelo que se desarrolle como tal.

El modelo se encuentra en el siguiente link:

(https://drive.google.com/file/d/1yHK3R4x5m-flUvCJVnpYnm8crXxJXzx8/view?usp=sharing)

## Datos_Modelo

Los desarrollos de los datos se encuentran en el notebook de Jupyter Datos_Modelo, hasta dejar un archivo llamado df creado a partir de los data frame df reviews y df_items
 a este dataframe que ya esta limpio ingresa para hacer otro dta frame piv con base en la función pivot_table  que convierte estos datos como en una tabla dinámica
 y la voltea para dejar en las filas los usuarios y en las columnas los juegos y co nlos datos del raiting con que cada jugado califico el juego.

Ya con esa tabla, se normalizan los valores por que es muy grande y difícil de entender y tiene valores discímiles, 
Para eso lo que se hizo fué los valores del dataframe piv restar la media de las calificaciones de un usuario y luego dividir
por la diferencia entre el valor máximo y mínimo de las calificaciones. Esto ajusta las calificaciones de un usuario 
y se centradan   en cero y escaladas en función de su variabilidad. 

Se borran los usuarios que no dieron todas las calificaciones de forma correcta, Esto se debe a que estos usuarios no aportan información útil para el modelo de recomendación si todas sus calificaciones son iguales o si solo tienen una calificación.

Luego seconvirtio en formato de matriz dispersa pues si no será un df muy grande

Data frame utilizado para el modelo: (https://drive.google.com/file/d/1u8krMhv4W5-K2wKGw576QZ-ttNCu2SBM/view?usp=sharing)

## Similitud del Coseno

Cuando se tiene la matriz dispersa, un poco mas digerible se utiliza la similitud del coseno haciendo 2 matrices de juegos donde se mida la similitud entre los datos o 
elementosy se clcula mediante el cosenodel angulo entre los dos vectores de elementos. 
Las dos maatrices fueron :item_sim_df y user_sim_df 

## Función de Recomendación

Con la relación calculada mediante el coseno, se hace una función que recomiende 5 juegos en función del juego que ingresó como argumento, teniendo en cuenta los valores
mas altos que generó el cálculo con el coseno,  organizando la similitud de mayor a menor y finalmente se se imprime la lista de juegos.


### Presentación

Se presenta un video con la funcionalidad que genera el proyecto y un breve resúmen de los pasos surtidos















