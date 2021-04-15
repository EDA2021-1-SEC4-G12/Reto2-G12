
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf

import argparse
parser = argparse.ArgumentParser(description='Testing colisions')

parser.add_argument('--type_cols', default='CHAINING', type=str)

args = parser.parse_args()


def initCatalog(type_cols, factor_C_CHAINING, factor_C_PROBING):
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog(type_cols, factor_C_CHAINING, factor_C_PROBING)


def loadData(catalog):
    """
    Carga los videos en el catalogo
    """
    controller.loadData(catalog)


#--------------------------------------------------------------------------------
## Test ##

fc_chaining = [2,4,6] 
fc_probing  = [0.3,0.5,0.8]

if args.type_cols == 'CHAINING':
    print('Cargando informacion de archivos con - CHAINING')
else:
    print('Cargando informacion de archivos con - PROBING')

for t_ in range(3):
    cont = controller.initCatalog(args.type_cols, fc_chaining[t_], fc_probing[t_])
    delta_t, delta_m = controller.loadData(cont)
    if args.type_cols == 'CHAINING':
        print('Vidoes cargados: ' + str(controller.videosSize(cont)))
        print('Factor de carga: ' + str(fc_chaining[t_]))
        print('Tiempo [ms]: ', '{:.3f}'.format(delta_t), '  ||  ',
              'Memoria [kB]: ', '{:.3f}'.format(delta_m) )
    elif args.type_cols == 'PROBING':
        print('Vidoes cargados: ' + str(controller.videosSize(cont)))
        print('Factor de carga: ' + str(fc_probing[t_]))
        print('Tiempo [ms]: ', '{:.3f}'.format(delta_t), '  ||  ',
              'Memoria [kB]: ', '{:.3f}'.format(delta_m) )