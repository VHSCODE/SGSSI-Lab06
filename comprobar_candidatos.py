#!/bin/python
## Actividad 1

from hashlib import sha256
import secrets

import sys

from os import listdir

from os.path import isfile, join



if len(sys.argv) < 3 :
    print("Por favor, especifica los archivos de entrada")
    exit(1)


buffer1 = []
buffer2 = []


with open(sys.argv[1],"rb") as f:
    buffer1 =f.read()

m = sha256()
m.update(buffer1)
hash_archivo1 = m.hexdigest()

fichero_con_ceros_maximos = ""
hash_fichero_ceros_maximo = ""
max_ceros = 0
# Obtenemos la lista de ficheros del directorio 
archivos_directorio = []

for f in listdir(sys.argv[2]): 
    if isfile(join(sys.argv[2],f)) :
        archivos_directorio.append(join(sys.argv[2],f))



for fichero in archivos_directorio:
    with open(fichero,"rb") as f:
        buffer2 =f.read()
    
    #Comprobamos si los contenidos del principio son los mismos
    m = sha256()
    m.update(buffer2[0:len(buffer1)])

    if hash_archivo1 != m.hexdigest():
        print(fichero + ": [FAIL: No coincide con el hash del archivo original]")
        continue
    
    #Comprobamos el contenido de la ultima linea

    ultima_linea = buffer2[len(buffer1):].decode()


    tokens= ultima_linea.split()

    if len(tokens) < 2:
        print(fichero + ": [FAIL:No contiene linea con codigo hexadecimal, identificador y cantidad de monedas]")
        continue


    elif tokens[2] != "100":
        print(fichero + ": [FAIL: Cantidad incorrecta de monedas]")
        continue


    #Finalmente comprobamos si el hash contiene una cadena de ceros al comienzo

    m = sha256()
    m.update(buffer2)

    cantidad_ceros = len(m.hexdigest()) - len(m.hexdigest().lstrip('0'))
    if cantidad_ceros <= 0:
        print(fichero + ": [FAIL: El hash del fichero no comienza por una lista de 0s]")
        continue
    elif(cantidad_ceros > max_ceros):
        max_ceros = cantidad_ceros
        fichero_con_ceros_maximos = fichero
        hash_fichero_ceros_maximo= m.hexdigest()
    print(fichero + ": [OK]")



print("Fichero con cadena de 0s mas larga: " + fichero_con_ceros_maximos)
print("Hash del fichero con ceros maximo:" + hash_fichero_ceros_maximo)
print("Cantidad de 0s: " + str(max_ceros))












