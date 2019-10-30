import tkinter as tk
from time import sleep
from tkinter import messagebox



intentos = 2

def aceptar():
	global intentos
	validas = ['15rg', '15gr']

	if intentos == 0:
		f.destroy()
		tk.Label(text='Has fallado!', font=("Courier", 18), fg='red').place(relx=0.5, rely=0.5, anchor=tk.CENTER)

	if e.get().lower() in validas:
		sleep(0.2)
		f.destroy()
		tk.Label(text='¡Felicidades!', font=("Courier", 18)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
	else:
		msg = 'Quedan {} intentos'.format(intentos)
		messagebox.showerror(title='Incorrecto', message=msg)
		var_advertencia.set(msg)
		intentos -=1

def dont_close(): #función que sobreescribe la acción de cerrar
	pass

root = tk.Tk()
root.attributes('-fullscreen', True) #pantlla completa

f = tk.Frame(master=root)
f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

tk.Label(master=f, text='Introduzca la contraseña').pack(fill=tk.X)

e = tk.Entry(master=f)
e.pack(fill=tk.X)

tk.Button(master=f, text='Introducir', command=aceptar).pack()

var_advertencia = tk.StringVar()
var_advertencia.set(' ')
tk.Label(master=f, textvariable=var_advertencia, fg='red').pack(fill=tk.X)

# root.protocol("WM_DELETE_WINDOW", dont_close) #redireccionar el click en la cruz para que no cierre
root.mainloop()