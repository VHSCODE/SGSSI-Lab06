#!/bin/python
## Actividad 3

from hashlib import sha256
import secrets
import sys
from os import listdir
from os.path import isfile, join
import random


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

# Obtenemos la lista de ficheros del directorio 
archivos_directorio = []
candidatos_a_sorteo=[]

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
        print(fichero + ": [FAIL] -> No coincide con el hash del archivo original")
        continue
    
    #Comprobamos el contenido de la ultima linea

    ultima_linea = buffer2[len(buffer1):].decode()


    tokens= ultima_linea.split()

    if len(tokens) < 2:
        print(fichero + ": [FAIL] -> No contiene linea con codigo hexadecimal, identificador y cantidad de monedas")
        continue


    elif tokens[2] != "100":
        print(fichero + ": [FAIL] -> Cantidad incorrecta de monedas]")
        continue


    #Finalmente comprobamos si el hash contiene una cadena de ceros al comienzo

    m = sha256()
    m.update(buffer2)

    cantidad_ceros = len(m.hexdigest()) - len(m.hexdigest().lstrip('0'))
    if cantidad_ceros <= 0:
        print(fichero + ": [FAIL] -> El hash del fichero no comienza por una lista de 0s")
        continue
    print(fichero + ": [OK]   -> Cantidad 0s = " + str(cantidad_ceros))

    #Añadimos el fichero a los candidatos
    candidatos_a_sorteo.append(fichero)




#Seleccionamos entre los candidatos de forma aleatoria

ganador = random.choice(candidatos_a_sorteo)

with open(ganador,"rb") as f:
        buffer2 =f.read()


m = sha256()
m.update(buffer2)

print("Ganador de sorteo: " + ganador)
print("Hash del fichero ganador:" + m.hexdigest())
print("Cantidad de 0s: " + str(len(m.hexdigest()) - len(m.hexdigest().lstrip('0'))))












