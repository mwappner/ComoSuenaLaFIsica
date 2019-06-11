# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 21:23:10 2018

@author: Marcos
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
aca = os.getcwd()
#%%
#fig, ax = plt.subplots()
#fig.set_tight_layout(True)
senos = []
x = np.linspace(0,np.pi,200)
#amplitudes para el trail en gris
y = np.cos(np.linspace(0,0.5*np.pi,8))
y = np.concatenate((y[::-1],-y[::-1]))

with plt.xkcd():
    fig,axes = plt.subplots(3,2,sharex=True,sharey=True)

    
    #graico los cuatro modos
    for k in range(1,5):
        ax = axes[np.unravel_index(k-1,axes.shape)]
    #    ax = plt.subplot(3,2,k)
    
        ax.axis('off')
        senos.append(np.sin(x*k)) #guardo el valor para este modo
        
        #grafico el trail en gris
        for amp in y:
            ax.plot(x,amp*senos[-1],color='0.7')
        
        #dibujo la soga
        ax.plot(x,senos[k-1],color = 'k',linewidth=2)

    
    #coeficientes de la suma
    coef1 = np.linspace(1,4,4)**-1 #lineal
    coef1 /= sum(coef1) #nomralizo
    coef2 = np.exp(np.linspace(0,-3,4)) #exponencial
    coef2 /= sum(coef2) #normalizo
    
    #creo sumas
    suma1 = sum([s*c for s,c in zip(senos,coef1)])
    suma2 = sum([s*c for s,c in zip(senos,coef2)])
    
    #grafico la primera suma
    ax = axes[np.unravel_index(4,axes.shape)]
    ax.axis('off')
    ax.plot(x,suma1,color = 'k',linewidth=2)
#    ax.plot(x,-suma1,color = 'k',linewidth=2)
    
    #grafico la segunda suma
    ax = axes[np.unravel_index(5,axes.shape)]
    ax.axis('off')
    ax.plot(x,suma2,color = 'k',linewidth=2)
#    ax.plot(x,-suma2,color = 'k',linewidth=2)

    #saco espacios en blanco y fijo eje y
    plt.subplots_adjust(wspace=1e-5,hspace=1e-5)
    ax.set_ylim(-1.2,1.2)

#ejes en una sola lista (se lo podria cambiar arriba, pero cero ganas)
ejeses = axes.flatten()

def update(t):
#    label = 'timestep {0}'.format(i)
    print('Instante {:.3f}s'.format(t))
    # Update the line and the axes (with a new xlabel). Return a tuple of
    # "artists" that have to be redrawn for this frame.
    
    amplitudes = [] #guarda la amplitud de cada modo
    for k,ax in enumerate(ejeses):
        if k == 4:
            ax.lines[-1].set_ydata(sum([s*c for s,c in zip(senos,coef1*amplitudes)]))
            continue
        if k == 5:
            ax.lines[-1].set_ydata(sum([s*c for s,c in zip(senos,coef2*amplitudes)]))
            continue
        
        amplitudes.append(np.cos(2*np.pi*t*(k+1)))
        print(k,amplitudes)
        ax.lines[-1].set_ydata(senos[k]*amplitudes[-1])

    
    return axes


tiempo = np.linspace(0,1,60)

if __name__ == '__main__':
    # FuncAnimation will call the 'update' function for each frame; here
    # animating over 10 frames, with an interval of 200ms between frames.
    anim = FuncAnimation(fig, update, frames=tiempo, interval=150,
                         repeat=True)
    plt.show()
#    if len(sys.argv) > 1 and sys.argv[1] == 'save':
#        anim.save(os.path.join(aca,'scatter.gif'), dpi=80, writer='imagemagick')
#    else:
#        # plt.show() will just loop the animation forever.
#        plt.show()
    anim.save(os.path.join(aca,'sogas.gif'), writer='imagemagick', fps=60)