# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 00:37:29 2019

@author: Marcos
"""

import simpleaudio as sa
import numpy as np

#%%

sr, duration, freq = 32000, 2, 150
time = np.linspace(0, duration, duration * sr, endpoint=False)
seno = (2**15-1) * np.sin(time * 2 * np.pi * freq)
seno = seno.astype(np.int16)

ply_this = sa.play_buffer(seno, 1, 2, sr)
ply_this.wait_done()

#%%
import tkinter as tk 


root = tk.Tk()
root.geometry('350x200')

def makesliders(base, tipo):
    toolbar = tk.Frame(master=base, relief=tipo, padx=3, pady=2, borderwidth=1)
    tk.Label(master=toolbar, text=str(tipo)).pack(side=tk.TOP)
    tk.Scale(master=toolbar).pack(side=tk.RIGHT)
    tk.Scale(master=toolbar).pack(side=tk.LEFT)
    toolbar.pack()

for tipo in (tk.SUNKEN, tk.RAISED, tk.GROOVE, tk.RIDGE, tk.FLAT): 
    makesliders(root, tipo)

root.mainloop()