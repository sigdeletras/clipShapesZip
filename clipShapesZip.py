#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nombre:
clipShapesZip.py

Autor:
Patricio Soriano :: SIGdeletras.com

Descripción:
Descomprime de forma temporal un zip con Shape Files
y recorta cada archivo shp a partir de una capa poligonal.

Requisistos:
    - Instalación de  Python2 o Python3
    - La librería GDAL
    - Es necesario indicar
        - Ruta/nombre de archivo zip
        - Ruta/nombre de capa de recorte
        - Ruta/nombre de carpeta de destino

Ejemplos:
    $ python clipShapesZip.py 'G15_Patrimonio.zip' 'clip_area.shp' 'clipFolder'

"""
import sys
import os
import shutil
from zipfile import ZipFile
try:
    from osgeo import ogr, osr, gdal
except ImportError:
    sys.exit(
        'ERROR: Paquetes GDAL/OGR no encontrados. '
        'Compruebe que están instalados correctamente')


def clipShapesZip(zipfile, clipshape, dirclip):

    path = dirclip

    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('Ya existe una carpeta \'%s\' en el directorio.' % (dirclip))
        print('Bórrela o indique otro nombre.')
        sys.exit()

    with ZipFile(zipfile) as myzip:  # Descomprime zip
        myzip.extractall()
    zipfilefolder = zipfile[0:-4:]  # Carpeta zip
    print('Descompresión de archivos en carpeta \'%s\' \n' % (zipfilefolder))
    for shapefile in os.listdir(zipfilefolder):
        if shapefile[-4:] == ".shp":
            shapefilename = shapefile[0:-4:]
            clipshapefilename = ''
            clipshapefilename = shapefilename+'_clip.shp'
            ogrclip = 'ogr2ogr -clipsrc %s %s %s' % (clipshape, path+'/'+clipshapefilename, zipfilefolder+"/"+shapefile)
            os.system(ogrclip)  # Clip
            print("Capa %s recortada en la carpeta %s" % (
                clipshapefilename, dirclip))
    shutil.rmtree(zipfilefolder)
    print('\nElimimnación de carpeta\'%s\'' % (zipfilefolder))

if __name__ == '__main__':
    zipfile = sys.argv[1]     # Archivo ZIP
    clipshape = sys.argv[2]  # Archivo DXF de origen
    dirclip = sys.argv[3]    # Archivo GML de salida
    clipShapesZip(zipfile, clipshape, dirclip)
