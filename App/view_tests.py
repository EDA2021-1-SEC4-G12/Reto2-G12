﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
import sys
import datetime
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar los Top videos por likes en categoría y país")
    print("3- Consultar el video con mas trending en pais")
    print("4- Consultar el video con mas trending en categoria")
    print("5- Consultar los Top videos por likes en pais dado tag")


def initCatalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog()


def loadData(catalog):
    """
    Carga los videos en el catalogo
    """
    controller.loadData(catalog)


def printTopLikes(videos, top):
    if (videos):
        print('El top ' + str(top) + ' de videos con más likes: ')
        for video in lt.iterator(videos):
            print('-------------------------------------------------------------------------' + \
                  '-------------------------------------------------------------------------')
            print('Trending (d): ' + video['trending_date'] + ' ||Titulo: ' + video['title'] + \
                  ' ||Published: ' + video['publish_time'] + ' ||Views: ' + video['views'] + \
                  ' ||Likes: ' + video['likes'] + ' ||Dislikes: ' + video['dislikes'])
        print('\n')
    else:
        print('No se encontraron videos')

def printTopTrendingCountry(video, top, days):
    if (video):
        print('El video más trending: ')
        print('-------------------------------------------------------------------------')
        print('Titulo: ' + video['title'] + ' ||Canal: ' + video['channel_title'] +\
                ' ||Pais: ' + video['country'] + ' ||Dias: ' + str(days))
        print('\n')
    else:
        print('No se encontraron videos')

def printTopTrendingCategory(video, top, days):
    if (video):
        print('El video más trending: ')
        print('-------------------------------------------------------------------------')
        print('Titulo: ' + video['title'] + ' ||Canal: ' + video['channel_title'] +\
                ' ||ID Categoria: ' + video['category_id'] + ' ||Dias: ' + str(days))
        print('\n')
    else:
        print('No se encontraron videos')


def printTopLikesTags(videos, top):
    if (videos):
        print('El top ' + str(top) + ' de videos con más likes: ')
        for video in lt.iterator(videos):
            print('-------------------------------------------------------------------------' + \
                  '-------------------------------------------------------------------------')
            print('Titulo: ' + video['title'] + ' ||Canal: ' + video['channel_title'] +\
                  ' ||Published: ' + video['publish_time'] + ' ||Views: ' + video['views'] + \
                  ' ||Likes: ' + video['likes'] + ' ||Dislikes: ' + video['dislikes'] + \
                  ' ||Tags: ' + video['tags'])
        print('\n')
    else:
        print('No se encontraron videos')

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        cont = controller.initCatalog()
        delta_t, delta_m = controller.loadData(cont)
        print("Cargando información de los archivos ....")
        print('Videos cargados: ' + str(controller.videosSize(cont)))
        print('Categorias cargadas: ' + str(controller.categoriesSize(cont)))
        print('Tiempo [ms]: ', f'{delta_t:.3f}', '  ||  ',
              'Memoria [kB]: ', f'{delta_m:.3f}')

    elif int(inputs[0]) == 2:
        n_videos = input('Top videos por likes: ')
        category = input('Categoría: ')
        country  = input('Pais: ')
        videosCategoryCountry = controller.getVideosByCategoryAndCountry(cont, category, country)
        topVideosLikes = controller.sortVideosLikes(videosCategoryCountry['videos'], int(n_videos))
        printTopLikes(topVideosLikes, int(n_videos))
        
    elif int(inputs[0]) == 3:
        country = input('Pais: ')
        videosCountry = controller.getVideosByCountry(cont, country)
        topTrendingVideo = controller.sortVideosTime(videosCountry['videos'], 100)
        topVidTD = datetime.datetime.strptime(lt.getElement(topTrendingVideo,0)['trending_date'], '%y.%d.%m')
        topVidPT = datetime.datetime.strptime(lt.getElement(topTrendingVideo,0)['publish_time'][:10], '%Y-%m-%d')
        daysTrending = topVidTD-topVidPT; daysTrending = int(daysTrending.days)
        printTopTrendingCountry(lt.getElement(topTrendingVideo,0),1,daysTrending)

    elif int(inputs[0]) == 4:
        category = input('Categoría: ')
        videosCategory = controller.getVideosByCategory(cont, category)
        topTrendingVideo = controller.sortVideosTime(videosCategory['videos'], 100)
        topVidTD = datetime.datetime.strptime(lt.getElement(topTrendingVideo,0)['trending_date'], '%y.%d.%m')
        topVidPT = datetime.datetime.strptime(lt.getElement(topTrendingVideo,0)['publish_time'][:10], '%Y-%m-%d')
        daysTrending = topVidTD-topVidPT; daysTrending = int(daysTrending.days)
        printTopTrendingCategory(lt.getElement(topTrendingVideo,0),1,daysTrending)

    elif int(inputs[0]) == 5:
        n_videos = input('Top videos por likes: ')
        tag = input('Tag: ')
        country = input('Pais: ')
        videosCountryTag = controller.getVideosByCountryAndTag(cont, country, tag)
        topVideosLikes = controller.sortVideosLikes(videosCountryTag['videos'], int(n_videos))
        printTopLikesTags(topVideosLikes, int(n_videos))
    
    else:
        sys.exit(0)
sys.exit(0)