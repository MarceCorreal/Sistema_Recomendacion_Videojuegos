<p align="center">
<img src="https://github.com/MarceCorreal/PI1_ML/blob/main/Assets/logo_steam%20(1).svg" />
</p>

<h1 align="center"><b>PROYECTO INDIVIDUAL 1 - MACHINE LEARNING - DPT07</b></h1>





## Generalidades del Repositorio

<p style="text-align: justify;">

El presente proyecto se presenta como requisito para la cursada de Henry

Consiste en desarrollar un sistema de recomendación de videojuegos de la tienda Steam, surtiendo todos los pasos que se deben tener en cuenta para esta misión.

El proyecto se desarrolla en VPython - VisualCode Studio

El repositorio de Henry con las consignas se encentran en: https://github.com/soyHenry/PI_ML_OPS/blob/FT/Readme.md

</p>




## Documentación
<p style="text-align: justify;">

En el Presente repositorio se encontrarán los notebooks de Jupyter en que se trabajan los datos y la programación del proyecto. 

Los documentos y data sets para la entrega se encontrarán además, en el siguiente Drive de Google creado para este fin:

[[https://drive.google.com/drive/folders/1npceA-nxhnUVxT3Y0qtKvKYyVYIIaaGL?usp=sharing](https://drive.google.com/drive/folders/13gMlg5p4hE9f6q6UP05ZRnvu3DlLbGvg?usp=drive_link)]

</p>


## Diagrama de Flujo del Proyecto


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












