# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 18:02:14 2019

@author: Marcos
"""

import numpy as np
import matplotlibpyplot as plt

#%%

cantx = 500 #densidad de puntos horizontal
canty = 20 #denisdad de puntos vertical

r = np.random.rand(cantx, canty)*2.4
x = np.linspace(0, 20, cantx)
s = np.sin(x) + 1.1
donde = np.array([r[:,i]<s for i in range(r.shape[-1])]).T

plt.plot(r[donde], 'k.')
y = np.random.rand(*r.shape)
y[donde] = np.nan

#with plt.xkcd():
fig, (ax1, ax2) = plt.subplots(2,1, sharex=True, squeeze=True, 
                         gridspec_kw={'height_ratios':(3,1)}) #para que el eje de arriba sea más chico
fig.set_size_inches([9, 2]) #tamaño de la figu
fig.subplots_adjust(hspace=0) #para que los ejes esten pegaditos

ax1.plot(x, y, 'k.')
ax1.axis('off')
ax2.plot(x, -s, lw=5)
ax2.set_ylim((0.1, -2.3))
ax2.axis('off')

fig.subplots_adjust(bottom = 0, top = 1, left = 0, right = 1)
plt.savefig('Figus/sonido.png', dpi=1000)
