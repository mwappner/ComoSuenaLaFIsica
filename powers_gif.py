# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 00:35:09 2018

@author: Marcos
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os
#%%
def plot_for_offset(power, y_max):
    # Data for plotting
    t = np.arange(0.0, 100, 1)
    s = t**power

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(t, s)
    ax.grid()
    ax.set(xlabel='X', ylabel='x^{}'.format(power),
           title='Powers of x')

    # IMPORTANT ANIMATION CODE HERE
    # Used to keep the limits constant
    ax.set_ylim(0, y_max)

    # Used to return the plot as an image rray
    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image

aca = os.getcwd()
kwargs_write = {'fps':1.0, 'quantizer':'nq'}
imageio.mimsave(os.path.join(aca,'powers.gif'), [plot_for_offset(i/4, 100) for i in range(10)], fps=1)