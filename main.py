""" 
Imagina que esta API es una biblioteca de peliculas:
La funcion load_movies() es como una biblioteca que carga el catalogo de libros (peliculas) cuando se abre la biblioteca.
La funcion get_movies() muestra todo el catalogo cuando alguien lo pide.
La funcion get_movie(id) es como si alguien preguntara por un libro especifico es decir, por un coidgo de identificacion.
La funcion chatbot (query) es un asistente que busca peliculas segun palabras clave y sinonimo.
La funcion get_movies_by_category(category) ayuda a encontrar peliculas segun su genero (accion, comedia, etc...)
"""

#Librerías
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd 
import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

#ruta de los datos 
nltk.data.path.append(r'C:\Users\Usuario\AppData\Roaming\nltk_data')
#nltk.download('punkt')
#nltk.download('wordnet')

#Funcion de carga de las peliculas desde el archivo .csv
def load_movies():
    df = pd.read_csv(r'C:\Users\Usuario\Desktop\T_tech\Proyecto\Dataset\netflix_titles.csv')[['Show_id', 'title','release_year','listened_in','rating','description']]
    
    #Renombramos las columnas 
    df.columns = ['id', 'title', 'year', 'category', 'rating', 'overview']
    