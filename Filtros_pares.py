# -*- coding: utf-8 -*-
"""
Filtros!
"""

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import random

#define parámetros de un filtro pasabajos a partir de:
#cutoff: frecuencia de corte
#fs: frecuencia de sampleo
#ordder: orden del filtro (ni idea, mirar la documentación)
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

#define el filtro en sí
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y



#%% Con los audios:

from scipy.io import wavfile
import os
import numpy as np

#lista para guardar los audios
audioFiles = []

#ubicación de los audios y de dónde voy a poner los filtrados:
#En la carpeta 'Originales' dentro del directorios donde está estre acrchivo
actual = os.getcwd()
audioPath = os.path.join(actual,'Nuevos')
#En el mismo directorio, en la carpeta Filtrados (no la crea)
filtradosPath = os.path.join(actual,'Pares Nuevos')

#carga nombres de los archivos
for file in os.listdir(audioPath):
    if file.endswith('.wav'):
        audioFiles.append(file)

audioFiles.sort() #ordeno

corte = 310 #freq de corte en Hz elegida a manopla a partir del espectro ("cerquita arriba de la fundamental")
orden = 9 #decidido de mirar varios valores con la visualización comentada
fundamental = 293 #elegida a manopla a partir del espectro


#aplico el filtro varias veces para que sea más abrupto
def variasVeces(datos,corte,sr,orden,veces=4):
    out = datos.copy()    
    for _ in range(veces):
        out = butter_lowpass_filter(out,corte,sr,orden)
    return out

#%% Para cada filtro, concateno todos los instrumentos filtrados

def porInsrumento(archivos,path,corte,fundamental,vez,cada=2,silencio_dur=0.25):
    #archivos: lisa con los nombres de los archivos sin filtrar
    #path: ubicación de los archivos
    #corte: la frecuencia de corte del filtro
    #funcamental: la frecuencia fundamental de datos
    #vez: determina qué filtro es (cuántos armónicos corresponde agregar esta vez)
    #cada: de a cuantos armónicos agrega cada vez que pasa un nuevo filtro
    #silencio_dur: duración del silencio entre un filtro y el siguiente, en segundos
    
    seno = np.sin(np.linspace(-np.pi/2,np.pi/2,8000))*.5
    for cual,file in enumerate(archivos):
        sr,datos = wavfile.read(os.path.join(path,file))
        datos = datos[:sr*2,0] #corto y me quedo con un segundo de datos
        nuevo = variasVeces(datos,corte+fundamental*cada*vez,sr,orden) #filtro
        envolvente = np.concatenate((.5 + seno,np.ones(len(datos)-2*len(seno)),.5-seno))
        nuevo *= envolvente
        silencio = np.zeros(int(sr*silencio_dur))
#        print('Convirtiendo '+file)
        if cual == 0:
            out = nuevo
        else:
            out = np.concatenate((out,silencio,nuevo))
    return out,sr

#lo aplico seis veces para agregar hasta el armónico 12 (el violín tiene muchos armónicos altos)

armonicos = [0,1,2,4,8]

#for k in range(20):

for k,vez in enumerate(armonicos*5):
    sample = random.sample(audioFiles,2)
    print('Seleccionado:',k,sample)
    f,sr = porInsrumento(sample,audioPath,corte,fundamental,vez,cada=1)
    f /= max(f)
    f *= 2**14
    f += np.random.normal(0,200,f.shape)
    f = np.asarray(f,dtype=np.int16)

    nombre =  'arm{} - {} - {}.wav'.format(vez,sample[0][:-4],sample[1][:-4])
    wavfile.write(os.path.join(filtradosPath,nombre),sr,f)
    
for k,vez in enumerate(armonicos*2):
    sample = [random.choice(audioFiles)]*2
    print('Seleccionado:',k,sample)
    f,sr = porInsrumento(sample,audioPath,corte,fundamental,vez,cada=1)
    f /= max(f)
    f *= 2**14 * random.uniform(.4,1.4)
    f += np.random.normal(0,200,f.shape)
    f = np.asarray(f,dtype=np.int16)

    nombre =  'arm{} - {} - {}.wav'.format(vez,sample[0][:-4],sample[1][:-4])
    wavfile.write(os.path.join(filtradosPath,nombre),sr,f)