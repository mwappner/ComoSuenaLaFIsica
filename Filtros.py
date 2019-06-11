# -*- coding: utf-8 -*-
"""
Filtros!
"""

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

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


#%% Visualizo el filtro con un ejemplito robado de stackoverflow
order = 20
fs = 30.0       # sample rate, Hz
cutoff = 3.667  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


# Demonstrate the use of the filter.
# First make some data to be filtered.
T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 1.2 Hz signal from this.
data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()

#%% Con los audios:

from scipy.io import wavfile
import os
import numpy as np

#lista para guardar los audios
audioFiles = []

#ubicación de los audios y de dónde voy a poner los filtrados:
#En la carpeta 'Originales' dentro del directorios donde está estre acrchivo
actual = os.getcwd()
audioPath = os.path.join(actual,'Originales')
#En el mismo directorio, en la carpeta Filtrados (no la crea)
filtradosPath = os.path.join(actual,'Filtrados')

#carga nombres de los archivos
for file in os.listdir(audioPath):
    if file.endswith('.wav'):
        audioFiles.append(file)

audioFiles.sort() #ordeno

corte = 750 #freq de corte en Hz elegida a manopla a partir del espectro ("cerquita arriba de la fundamental")
orden = 10 #decidido de mirar varios valores con la visualización comentada
fundamental = 522 #elegida a manopla a partir del espectro

########### PARA VISIALIZAR EL FILTRO
# Get the filter coefficients so we can check its frequency response.
#b, a = butter_lowpass(corte, sr, orden)

# Plot the frequency response.
#w, h = freqz(b, a, worN=8000)
#plt.subplot(2, 1, 1)
#plt.plot(0.5*sr*w/np.pi, np.abs(h), 'b')
#plt.plot(corte, 0.5*np.sqrt(2), 'ko')
#plt.axvline(corte, color='k')
#plt.xlim(0, 0.5*sr)
#plt.title("Lowpass Filter Frequency Response")
#plt.xlabel('Frequency [Hz]')
#plt.grid()
##############

#aplico el filtro varias veces para que sea más abrupto
def variasVeces(datos,corte,sr,orden,veces=4):
    out = datos.copy()    
    for _ in range(veces):
        out = butter_lowpass_filter(out,corte,sr,orden)
    return out

#%% Corro el filtro para distintas frecuencias de corte para cada instrumento
    

def filtrosVarios(datos,corte,fundamental,sr,cada=2,veces=4,silencio_dur=0.25):
    #datos: el archivo a filtrar
    #corte: la frecuencia de corte del filtro
    #funcamental: la frecuencia fundamental de datos
    #sr: frecuencia de muestreo
    #cada: de a cuantos armónicos agrega cada vez que pasa un nuevo filtro
    #veces: cuántos filtros distintos crea
    #silencio_dur: duración del silencio entre un filtro y el siguiente, en segundos
    
    maximo = np.max(np.abs(datos)) #para escalar los filtrados y equiparar volumen
    silencio = np.zeros(int(sr*silencio_dur)) #crea el cilencio
    for k in range(veces):
        nuevo = variasVeces(datos,corte+fundamental*cada*k,sr,orden) #sonido filtroado
        nuevo = nuevo / np.max(nuevo) * maximo #arregla volumen
        
        #concantena sonidos
        if k==0:
            out = nuevo
        else:
            out = np.concatenate((out,silencio,nuevo))
    return out

#aplico los filtros a todos los instrumentos
for cual,file in enumerate(audioFiles):

    sr,datos = wavfile.read(os.path.join(audioPath,file)) #devuelve el sonido y la frecuencia de muestreo
    
    datos = datos[:sr*2] #corto y me quedo con dos segundos de sonido
        
    todo= filtrosVarios(datos,corte,fundamental,sr,veces=12)#aplico filtro
    todo = np.asarray(todo,dtype=np.int16)#por un tema de compaibilidad con el formato
    #plt.plot(todo)
    
    wavfile.write(os.path.join(filtradosPath,file[:-4]+'_filtrado.wav'),sr,todo)#guardo el sonido

#%% Para cada filtro, concateno todos los instrumentos filtrados

def porInsrumento(archivos,path,corte,fundamental,vez,cada=2,silencio_dur=0.25):
    #archivos: lisa con los nombres de los archivos sin filtrar
    #path: ubicación de los archivos
    #corte: la frecuencia de corte del filtro
    #funcamental: la frecuencia fundamental de datos
    #vez: determina qué filtro es (cuántos armónicos corresponde agregar esta vez)
    #cada: de a cuantos armónicos agrega cada vez que pasa un nuevo filtro
    #silencio_dur: duración del silencio entre un filtro y el siguiente, en segundos

    for cual,file in enumerate(archivos):
        sr,datos = wavfile.read(os.path.join(path,file))
        datos = datos[:sr*2] #corto y me quedo con un segundo de datos
        nuevo = variasVeces(datos,corte+fundamental*cada*vez,sr,orden) #filtro
        silencio = np.zeros(int(sr*silencio_dur))
        print('Convirtiendo '+file)
        if cual == 0:
            out = nuevo
        else:
            out = np.concatenate((out,silencio,nuevo))
    return out

#lo aplico seis veces para agregar hasta el armónico 12 (el violín tiene muchos armónicos altos)
for k in range(6):
    f = porInsrumento(audioFiles,audioPath,corte,fundamental,k) *2
    f = np.asarray(f,dtype=np.int16)
    
    wavfile.write(os.path.join(filtradosPath,'f{}.wav'.format(k)),sr,f)