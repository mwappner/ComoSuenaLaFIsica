# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 14:32:49 2018

@author: Marcos
"""

import matplotlib.pyplot as plt
import numpy as np
#%%

with plt.xkcd():
    fg,axes = plt.subplots(3,2,sharex=True)
    x = np.linspace(0,np.pi,200)
    y = np.cos(np.linspace(0,0.5*np.pi,8))
#    y = np.delete(y,0)
    y = np.concatenate((y[::-1],-y[::-1]))
    senos = []
    
    for k in range(1,5):
        ax = axes[np.unravel_index(k-1,axes.shape)]
    #    ax = plt.subplot(3,2,k)
    
        ax.axis('off')
        for amp in y:
            ax.plot(x,amp*np.sin(x*k),color='0.7')
        
        senos.append(np.sin(x*k))
#        ax.plot(x,senos[k-1],color = 'k',linewidth=2)
#        ax.plot(x,-senos[k-1],color = 'k',linewidth=2)
#        plt.xkcd()
        ax.set_ylim(-1.2,1.2)

    coef1 = np.linspace(1,4,4)**-1
    coef2 = np.exp(np.linspace(0,-3,4))
    
    suma1 = sum([s*c for s,c in zip(senos,coef1)])
    suma1 /= max(suma1)
    suma2 = sum([s*c for s,c in zip(senos,coef2)])
    suma2 /= max(suma2)
    
    ax = axes[np.unravel_index(4,axes.shape)]
#    plt.xkcd()
    ax.axis('off')
    ax.plot(x,suma1,color = 'k',linewidth=2)
    ax.plot(x,-suma1,color = 'k',linewidth=2)
    ax.set_ylim(-1.2,1.2)
    
    ax = axes[np.unravel_index(5,axes.shape)]
#    plt.xkcd()
    ax.axis('off')
    ax.plot(x,suma2,color = 'k',linewidth=2)
    ax.plot(x,-suma2,color = 'k',linewidth=2)
    ax.set_ylim(-1.1,1.1)
    
    plt.subplots_adjust(wspace=1e-5,hspace=1e-5)

plt.show()