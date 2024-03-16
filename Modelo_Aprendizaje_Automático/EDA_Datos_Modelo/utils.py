
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