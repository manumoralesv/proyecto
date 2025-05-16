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
    
    #Llenamos los espacios vacíos con el texto 'vacío' y convertimos los datos en diccionarios
    return df.fillna('').to_dict(orient='records')
#cargamos las películas al iniciar la API para no leer el archivo cada que alguien pregunta por ellas.
movies_list = load_movies()

#funcion para encontrar sinónimos de una palabra
def get_synonyms(word):
    #Usamos WorldNet para obtener distintas palabras que significan lo mismo.
    return{lemma.name().lower() for syn in wordnet.synsets(word) for lemma in syn.lemmas()}
