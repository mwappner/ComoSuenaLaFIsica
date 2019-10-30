import tkinter as tk
from tkinter import ttk

modos = ['Saludo', 'Reto', 'uno muy muy muy largo']

root = tk.Tk()
tk.Label(master=root, text='Modo:').pack(fill=tk.X)
cb = ttk.Combobox(root, state='readonly', values=modos, 
                  width=max([len(m) for m in modos]))
cb.set(modos[0])
cb.bind("<<ComboboxSelected>>", lambda *a: print(cb.get()))
cb.pack(fill=tk.X)

e = tk.Entry(root)
e.pack()

def agregar(modos):
	modos += [e.get()]
	cb['values']= modos
	print(modos)

tk.Button(root, text='Agregar', command=lambda: agregar(modos)).pack()

root.mainloop()