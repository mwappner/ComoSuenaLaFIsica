# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 00:37:29 2019

@author: Marcos
"""

# import simpleaudio as sa
# import numpy as np

# #%%

# sr, duration, freq = 32000, 2, 150
# time = np.linspace(0, duration, duration * sr, endpoint=False)
# seno = (2**15-1) * np.sin(time * 2 * np.pi * freq)
# seno = seno.astype(np.int16)

# ply_this = sa.play_buffer(seno, 1, 2, sr)
# ply_this.wait_done()

#%%
import tkinter as tk 
from tkinter import ttk


root = tk.Tk()
root.geometry('350x200')

s = ttk.Scale(root)
s.pack()

ttk.Button(root, text='Activar', command= lambda: s.state(['!disabled'])).pack()

ttk.Button(root, text='Desactivar', command= lambda: s.state(['disabled'])).pack()

root.mainloop()