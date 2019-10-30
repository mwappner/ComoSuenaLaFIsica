# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 23:26:02 2018

@author: Marcos
"""

#import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os

#%%


def plot_for_offset(amplitud):
    # Data for plotting

    with plt.xkcd():
        fg,axes = plt.subplots(3,2,sharex=True)
        x = np.linspace(0,np.pi,200)
        y = np.cos(np.linspace(0,0.5*np.pi,8))
#        y = np.delete(y,0)
        y = np.concatenate((y,-y))
        senos = []
        
        for k in range(1,5):
            ax = axes[np.unravel_index(k-1,axes.shape)]
        #    ax = plt.subplot(3,2,k)
        
            ax.axis('off')
            for amp in y:
                ax.plot(x,amp*np.sin(x*k),color='0.7')
            
            senos.append(np.sin(x*k))
            ax.plot(x,senos[k-1],color = 'k',linewidth=2)
            ax.plot(x,-senos[k-1],color = 'k',linewidth=2)
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

#plt.show()

        # IMPORTANT ANIMATION CODE HERE
        # Used to keep the limits constant
        ax.set_ylim(0, y_max)
    
        # Used to return the plot as an image rray
        fig.canvas.draw()       # draw the canvas, cache the renderer
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image

kwargs_write = {'fps':1.0, 'quantizer':'nq'}
imageio.mimsave('./powers.gif', [plot_for_offset(i/4, 100) for i in range(10)], fps=1)