""" 
Imagina que esta API es una biblioteca de peliculas:
La funcion load_movies() es como una biblioteca que carga el catalogo de libros (peliculas) cuando se abre la biblioteca.
La funcion get_movies() muestra todo el catalogo cuando alguien lo pide.
La funcion get_movie(id) es como si alguien preguntara por un libro especifico es decir, por un coidgo de identificacion.
La funcion chatbot (query) es un asistente que busca peliculas segun palabras clave y sinonimo.
La funcion get_movies_by_category(category) ayuda a encontrar peliculas segun su genero (accion, comedia, etc...)
"""

#Librerías
from http.client import HTTPException
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd 
import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

#ruta de los datos 
nltk.data.path.append(r'C:\Users\Usuario\AppData\Roaming\nltk_data')
nltk.download('punkt_tab')
nltk.download('wordnet')

#Funcion de carga de las peliculas desde el archivo .csv
def load_movies():
    df = pd.read_csv(r'C:\Users\Usuario\Desktop\T_tech\Proyecto\Dataset\netflix_titles.csv')[['show_id', 'title','release_year','listed_in','rating','description']]
    
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

#creamos la aplicacion FastAPI, que será el motor de nuestra API
#Esto inicializa la API con un nombre y una version
app = FastAPI(title='Mi aplicación de Películas', version = '1.0.0')

#Ruta de inicio
@app.get("/", tags=['Home'])
def home():
    #cuando entremos en el navegador a http://127.0.0.1:8000/ veremos un mensaje de bienvenida
    return HTMLResponse("<h1>Bienvenido a la API de Películas</h1><p>Esta API te permite buscar películas por título, año, categoría y más.</p>")
    #obteniendo la lista de películas
    #Creamos una ruta para obtener todas las películas

#Ruta para obtener todas las películas disponibles 
@app.get('/movies', tags=['Movies'])
def get_movies():
    #Si hay peliculas, las enviamos, si no, mostramos un error
    return movies_list or HTTPException(status_code=500, detail= 'No hay datos de películas disponibles')

#Ruta para obtener una película específica según su ID
@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: str):
    #buscamos en la lista de películas la que tenga el mismo id
    return next((m for m in movies_list if m[id] ==id), {'detalle': 'película no encontrada'})

#Ruta del chatbot que responda 
@app.get('/chatbot', tags=['Chatbot'])
def chatbot(query: str):
    #dividimos la consulta en palabras clave para entender mejor la intensión del usuario
    query_words = word_tokenize(query.lower())
    
    #buscamos sinónimos de las palabras clave par aampliar la búsqueda
    synonyms = {word for q in query_words for word in get_synonyms(q)} | set(query_words)
    #filtramos la lista de películas buscando coincidencias en la categoría
    results = [m for m in movies_list if any (s in m['category'].lower() for s in synonyms)]
    
    #Si encontramos películas, enviamos la lista, si no, mostramos un mensaje de que no se encontraron coincidencias
    
    return JSONResponse (content ={
        'respuesta': 'Aquí tienes algunas películas relacionadas.' if results else 'No encontré películas en esa categoría',
        'películas': results
    })
    
#Ruta para obtener películas por categoría especifica 

@app.get('/movies/by_category/', tags=['Movies'])
def get_movies_by_category(category: str):
    #filtramos la lista de películas según la categoría ingresada
    return [m for m in movies_list if category.lower() in m['category'].lower()]