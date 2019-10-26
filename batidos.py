# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 15:15:39 2019

@author: Marcos
"""

import matplotlib.pyplot as plt
import numpy as np
#%%

#creo los senos con distintas frecuencias
x = np.linspace(0, 1000, 5000)
s1 = np.sin(x/(2*np.pi))
s2 = np.sin(1.1 * x/(2*np.pi))
envolvente = 2 * np.cos(0.05 * x/(2*np.pi))

# creo la figu con los dos ejes
fig, axes = plt.subplots(2,1, sharex=True, squeeze=True, 
                         gridspec_kw={'height_ratios':(2,3)}) #para que el eje de arriba sea más chico
fig.set_size_inches([10, 4]) #tamaño de la figu
fig.subplots_adjust(hspace=0) #para que los ejes esten pegaditos

#grafico senos
axes[0].plot([0]*s1.size, color='k') #línea horizonal
axes[0].plot(s1, color='C2', linewidth=2)
axes[0].plot(s2, color='C0', linewidth=2)
axes[0].axis('off') #apago la visibilidad

#grafico resultante y envolventes
axes[1].plot(s1+s2, color='C1', linewidth=2)
axes[1].plot(envolvente, '--', color='silver')
axes[1].plot(-envolvente, '--', color='silver')
axes[1].axis('off') #apago la visibilidad

plt.savefig('Figus/batidos.png', dpi=500)
#%% Repito con formato xkcd

with plt.xkcd(): #para el formato bonito de xkcd

    #creo los senos con distintas frecuencias
    x = np.linspace(0, 1000, 5000)
    s1 = np.sin(x/(2*np.pi))
    s2 = np.sin(1.1 * x/(2*np.pi))
    envolvente = 2 * np.cos(0.05 * x/(2*np.pi))
    
    # creo la figu con los dos ejes
    fig, axes = plt.subplots(2,1, sharex=True, squeeze=True, 
                             gridspec_kw={'height_ratios':(2,3)}) #para que el eje de arriba sea más chico
    fig.set_size_inches([10, 4]) #tamaño de la figu
    fig.subplots_adjust(hspace=0) #para que los ejes esten pegaditos
    
    #grafico senos
    axes[0].plot([0]*s1.size, color='k') #línea horizonal
    axes[0].plot(s1, color='C2', linewidth=2)
    axes[0].plot(s2, color='C0', linewidth=2)
    axes[0].axis('off') #apago la visibilidad
    
    #grafico resultante y envolventes
    axes[1].plot(envolvente, '--', color='silver')
    axes[1].plot(-envolvente, '--', color='silver')
    axes[1].plot(s1+s2, color='C1', linewidth=2)
    axes[1].axis('off') #apago la visibilidad
    
    plt.savefig('Figus/batidos_xkcd.png', dpi=500)