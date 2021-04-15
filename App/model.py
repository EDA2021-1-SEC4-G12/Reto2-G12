"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from App.controller import initCatalog
import config as cf
import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(type_list='ARRAY_LIST'):
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    if type_list != 'SINGLE_LINKED' and type_list != 'ARRAY_LIST':
        print('Invalid type')

    catalog = {'videos':None,
               'videoIDs':None,
               'categories':None,
               'categoryIDs':None,
               'countries':None}

    catalog['countries'] = mp.newMap(200,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareCountriesByName)

    catalog['videos'] = lt.newList(type_list, cmpvideoid)

    catalog['videoIDs'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMapVideoIds)

    catalog['categories'] = mp.newMap(34500,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=compareCategoryNames)

    catalog['categoryIDs'] = mp.newMap(34500,
                                       maptype='CHAINING',
                                       loadfactor=4.0,
                                       comparefunction=compareCategoryIds)


    return catalog


def newCategory(name, id):
    """
    Esta estructura crea una relación entre una caterogia y los videos que han sido
    marcados con dicha categoria.  Se guarga el total de videos y una lista con
    dichos videos.
    """
    category = {'name': '',
                'category_id': '',
                'total_videos': 0,
                'videos': None}
    category['name'] = name
    category['category_id'] = id
    category['videos'] = lt.newList()
    return category

def newCountry(name):
    """
    Esta estructura crea una relación entre una pais y los videos que han sido
    marcados con dicho pais.  Se guarga el total de videos y una lista con
    dichos videos.
    """
    country = {'name': '',
               'videos': None}
    country['name'] = name
    country['videos'] = lt.newList()
    return country

def newVideoID(id):
    """
    Esta estructura crea una relación entre una pais y los videos que han sido
    marcados con dicho pais.  Se guarga el total de videos y una lista con
    dichos videos.
    """
    country = {'id': '',
               'video': None}
    country['id'] = id
    country['video'] = lt.newList()
    return country

def addVideo(catalog, video):
    lt.addLast(catalog['videos'], video)
    country = video['country']
    addVideoCountry(catalog, str(country), video)
    # vidID = video['video_id']
    # addVideoID(catalog, str(vidID), video)


def addCategory(catalog, category):
    """
    Adiciona una categoria a la tabla de categorias dentro del catalogo y se
    actualiza el indice de identificadores de la categoria.
    """
    newcategory = newCategory(category['name'], category['id'])
    mp.put(catalog['categories'], category['name'], newcategory)
    mp.put(catalog['categoryIDs'], category['id'], newcategory)


def addVideoCategory(catalog, category):
    """
    Agrega una relación entre un libro y un tag.
    Para ello se adiciona el libro a la lista de libros
    del tag.
    """
    categoryid = category['id']
    categoryname = category['name']
    entry = mp.get(catalog['categoryIDs'], categoryid)

    for v_i in range(catalog['videos']['size']):
        video_i = lt.getElement(catalog['videos'], v_i)
        vid_i_category = video_i['category_id']
        categoryvideo = mp.get(catalog['categories'], me.getValue(entry)['name'])
        if categoryid == vid_i_category:
            lt.addLast(categoryvideo['value']['videos'],video_i)


def addVideoCountry(catalog, countryname, video):
    """
    Esta función adiciona un video a la lista de videos publicados
    en un pais.
    """
    countries = catalog['countries']
    existcountry = mp.contains(countries, countryname)
    if existcountry:
        entry = mp.get(countries, countryname)
        country = me.getValue(entry)
    else:
        country = newCountry(countryname)
        mp.put(countries, countryname, country)
    lt.addLast(country['videos'], video)


def addVideoID(catalog, id, video):
    """
    Esta función adiciona un video a la lista de videos publicados
    en un pais.
    """
    ids = catalog['video_id']
    existsID = mp.contains(ids, id)
    if existsID:
        entry = mp.get(ids, id)
        vidID = me.getValue(entry)
    else:
        vidID = newVideoID(id)
        mp.put(ids, id, vidID)
    lt.addLast(vidID['video'], video)

# Funciones para creacion de datos

# Funciones de consulta

def getVideosByCategory(catalog, categoryname):
    """
    Retornar la lista de videos asociados a una categoria
    """
    new_catalog = initCatalog()
    category = mp.get(catalog['categories'], categoryname)
    videos = None
    if category:
        videos = me.getValue(category)['videos']
        for vid_i in lt.iterator(videos):
            addVideo(new_catalog,vid_i)
    return new_catalog

def getVideosByCountry(catalog, countryname):
    """
    Retornar la lista de videos asociados a un pais
    """
    new_catalog = initCatalog()
    country = mp.get(catalog['countries'], countryname)
    videos = None
    if country:
        videos = me.getValue(country)['videos']
        for vid_i in lt.iterator(videos):
            addVideo(new_catalog,vid_i)
    return new_catalog

def getVideosByCategoryAndCountry(catalog, categoryname, countryname):
    """
    Retornar la lista de videos asociados a una categoria y un país
    """
    videosCategory = getVideosByCategory(catalog, categoryname)
    videosCatCountry = getVideosByCountry(videosCategory, countryname)
    return videosCatCountry

def getVideosByCountryAndTag(catalog, countryname, tag):
    """
    Retornar la lista de videos asociados a una categoria y un tag
    """
    tag = tag.lower() # make lowercase
    new_catalog = initCatalog()
    country = mp.get(catalog['countries'], countryname)
    tagexists = False
    if country:
        videos = me.getValue(country)['videos']
        for vid_i in lt.iterator(videos):
            vid_i_tags = vid_i['tags'].replace('"','').lower() # make lowercase
            vid_i_tags = vid_i_tags.split("|")
            for tag_kw in vid_i_tags:   # compare with specified tag
                if tag in tag_kw.split():
                    tagexists = True
            if tagexists:    
                addVideo(new_catalog,vid_i)
    return new_catalog

def videosSize(catalog):
    """
    Número de videos en el catago
    """
    return lt.size(catalog['videos'])

def categoriesSize(catalog):
    """
    Número de categorias en el catago
    """
    return lt.size(catalog['categories'])

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpvideoid(video1,video2):
    if (video1.lower() in video2['video_id'].lower()):
        return 0
    return -1

def compareCategoryIds(id, cat_id):
    cat_identry = me.getKey(cat_id)
    if (int(id) == int(cat_identry)):
        return 0
    elif (int(id) > int(cat_identry)):
        return 1
    else:
        return 0

def compareCategoryNames(name, cat_name):
    cat_identry = me.getKey(cat_name)
    if (name == cat_identry):
        return 0
    elif (name > cat_identry):
        return 1
    else:
        return -1

def compareMapVideoIds(id, entry):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1

def compareCountriesByName(keyname, country):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    contru_entry = me.getKey(country)
    if (keyname == contru_entry):
        return 0
    elif (keyname > contru_entry):
        return 1
    else:
        return -1



def cmpVideosByLikes(video1,video2):
    """
    Devuelve verdadero (True) si los 'views' de video1 son menores que los del video2
    Args:
        video1: informacion del primer video que incluye su valor 'views'
        video2: informacion del segundo video que incluye su valor 'views'
    """
    return (float(video1['likes']) > float(video2['likes']))

def cmpVideosByTime(video1,video2):
    """
    Devuelve verdadero (True) si los 'views' de video1 son menores que los del video2
    Args:
        video1: informacion del primer video que incluye su valor 'views'
        video2: informacion del segundo video que incluye su valor 'views'
    """
    time1_b = datetime.datetime.strptime(video1['trending_date'], '%y.%d.%m')
    time1_a = datetime.datetime.strptime(video1['publish_time'][:10], '%Y-%m-%d')
    days1 = time1_b-time1_a
    time2_b = datetime.datetime.strptime(video2['trending_date'], '%y.%d.%m')
    time2_a = datetime.datetime.strptime(video2['publish_time'][:10], '%Y-%m-%d')
    days2 = time2_b-time2_a
    return int(days1.days) < int(days2.days)


# Funciones de ordenamiento

def sortVideosLikes(catalog, size):
    sub_list = lt.subList(catalog, 0, size)
    #sub_list = sub_list.copy()
    sorted_list = sa.sort(sub_list, cmpVideosByLikes)
    return sorted_list

def sortVideosTime(catalog, size):
    sub_list = lt.subList(catalog, 0, size)
    sub_list = sub_list.copy()
    sorted_list = sa.sort(sub_list, cmpVideosByTime)
    return sorted_list