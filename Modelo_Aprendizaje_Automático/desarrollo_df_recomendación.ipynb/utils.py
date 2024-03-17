
# Importaciones de bibliotecas necesarias
import pandas as pd  # Pandas para manipulación de datos tabulares
import json  # Módulo para trabajar con JSON
import ast  # Módulo para evaluar expresiones literales de Python
import re  # Módulo para trabajar con expresiones regulares
from textblob import TextBlob # Importa la clase TextBlob desde la biblioteca TextBlob
import nltk # Importa la biblioteca nltk (Natural Language Toolkit)
import csv # Importa el módulo csv en Python

# Importa el módulo de advertencias y configura para ignorar todas las advertencias
import warnings
warnings.filterwarnings("ignore")


'''Función resumen_cant_porcentaje'''

# Lo que hace esta función es contar las ocurencias de cada registro
# y luego sacer el porcentaje de ese registro sobre el total. se va a 
# utilizar en el notebook del eda_datos_modelo

def resumen_cant_porcentaje(df, columna):
    # Cuenta la cantidad de True/False luego calcula el porcentaje
    counts = df[columna].value_counts()
    percentages = round(100 * counts / len(df),2)
    # Crea un dataframe con el resumen
    df_results = pd.DataFrame({
        "Cantidad": counts,
        "Porcentaje": percentages
    })
    return df_results
    pass

'''Función calcula_rating'''

# Esta función calcula el raiting de cada juego teniendo en cuenta si el sentimiento es negativo, neutro 
# o positivo y si es recomendado o no

def calcula_rating(row):
    
    if row["sentiment_analysis"] == 0 and not row["reviews_recommend"]:
        return 1
    elif row["sentiment_analysis"] == 0 and row["reviews_recommend"]:
        return 1
    elif row["sentiment_analysis"] == 1 and not row["reviews_recommend"]:
        return 2
    elif row["sentiment_analysis"] == 1 and row["reviews_recommend"]:
        return 3
    elif row["sentiment_analysis"] == 2 and not row["reviews_recommend"]:
        return 4
    elif row["sentiment_analysis"] == 2 and row["reviews_recommend"]:
        return 5
    else:
        return None