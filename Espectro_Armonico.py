#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 03:11:58 2019

@author: augusto
"""

#%%
from scipy.io import wavfile
import numpy as np
# import matplotlib.pyplot as plt
from scipy.fftpack import fft,fftfreq
import os
#%%

#Extracción de la data y gráfico de la misma:

carpeta = 'Voces'
archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta)]


def buscapicos(x,y,N):
    #N es el numero de armónicos que me interesan
    I=[] #Intensidades
    
    #EL umbral es la intensidad mínima que debe tener el primer pico para identificarlo como la fundamental. 
    #Este numero esta para que el programa pueda detectar la fundamental en el caso general,incluso cuando
    #la fundamental no es el armónico mas intenso.
    umbral=50 
    
    #Este 'for' esta para identificar la frecuencia fundamental
    for i in range(len(x)):
        if y[i]>umbral:
            fundamental=x[i]
            break
    #Este 'for' crea la lista de intensidades de cada armónico I 
    for j in range(N):
        
        # start_n y finish_n son los extremos de el intervalo donde el máximo es el armónico j-ésimo
        start_n=((j+1)*fundamental)-(fundamental/2)
        finish_n=((j+1)*fundamental)+(fundamental/2)
        
        #start_i y finish_i son los índices asociados a las frecuencias start_n y finish_n
        start_i=np.ndarray.tolist(x).index(min(x, key=lambda x:abs(x-start_n)))
        finish_i=np.ndarray.tolist(x).index(min(x, key=lambda x:abs(x-finish_n)))
        
        #interv son los valores de y en el intervalo que va desde la frecuencia start_n hasta finish_n
        interv=y[start_i:finish_i]
        
        #El máximo en interv es la intensidad del armónico j-ésimo
        I.append(interv.max() if interv.size else 0)
    return fundamental, I

archivo = os.path.join(carpeta, 'espectros_voces.txt')
with open(archivo, 'w') as f:

        for este in archivos:
            if este.endswith('txt'):
                continue
            print(este)

            samplerate, data = wavfile.read(este)
            # plt.plot(data[:200])
            # plt.grid()
            #%%

            #Transformada de Fourier y gráfico de la misma:

            datafft = fft(data)
            #Valor absoluto de la componente real y compleja:
            fftabs = abs(datafft)
            samples = data.shape[0]
            freqs = fftfreq(samples,1/samplerate)
            # plt.plot(freqs,fftabs)
            # plt.grid()
            #%%

            #Gráfico de las frecuencias positivas del espectro con x en escala logarítmica y amplitud normalizada a 100:

            # plt.xlim( [10, samplerate/2] )
            # plt.xscale( 'log' )
            # plt.grid( True )
            # plt.xlabel( 'Frequency (Hz)' )
            x=freqs[:int(freqs.size/2)]
            y=fftabs[:int(freqs.size/2)]
            y=y/max(y)
            y=y*100
            # plt.plot(x,y)
            # plt.grid()

            #%%

            #Defino una función para saber la intensidad de los N armónicos que me interesan:


            fund, ints = buscapicos(x,y,20)
            ints = [str(np.round(f,1)) for f in ints]
            
            f.write(os.path.basename(este))
            f.write(': {} Hz\n'.format(fund))
            f.write(', '.join(ints))
            f.write('\n')
