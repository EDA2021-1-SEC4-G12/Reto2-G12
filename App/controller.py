﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
import time
import tracemalloc
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos


def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadVideos(catalog)
    loadIDs(catalog)
    loadVideoCategories(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return delta_time, delta_memory


def loadVideos(catalog):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    videosfile = cf.data_dir + 'videos-5pct.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)


def loadIDs(catalog):
    # Carga todos los tags del archivo y los agrega a la lista de tags
    idsfile = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(idsfile, encoding='utf-8'))
    for id in input_file:
        model.addCategory(catalog, id)


def loadVideoCategories(catalog):
    idsfile = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(idsfile, encoding='utf-8'))
    for id in input_file:
        model.addVideoCategory(catalog, id)


# Funciones de ordenamiento

def sortVideosLikes(catalog, size):
    """
    Ordena los videos por likes
    """
    return model.sortVideosLikes(catalog, size)

def sortVideosTime(catalog, size):
    """
    Ordena los videos por views
    """
    return model.sortVideosTime(catalog, size)


# Funciones de consulta sobre el catálogo

def videosSize(catalog):
    """
    Numero de videos cargados al catalogo
    """
    return model.videosSize(catalog)

def categoriesSize(catalog):
    """
    Numero de categorias cargadas al catalogo
    """
    return model.categoriesSize(catalog)

def getVideosByCategory(catalog, category):
    """
    Retorna los videos dada una categoria
    """
    videos = model.getVideosByCategory(catalog, category)
    return videos

def getVideosByCountry(catalog, country):
    """
    Retorna los videos dado un pais
    """
    videos = model.getVideosByCountry(catalog, country)
    return videos

def getVideosByCategoryAndCountry(catalog, categoryname, countryname):
    """
    Retorna los videos dado una categoria y pais
    """
    videos = model.getVideosByCategoryAndCountry(catalog, categoryname, countryname)
    return videos

def getVideosByCountryAndTag(catalog, countryname, tag):
    """
    Retorna los videos dado un pais y tag
    """
    videos = model.getVideosByCountryAndTag(catalog, countryname, tag)
    return videos

# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory