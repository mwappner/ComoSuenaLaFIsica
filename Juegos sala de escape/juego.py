import tkinter as tk
from time import sleep
from tkinter import messagebox

fuente_universal = ('Helvetica', 16)

class Ventana1(tk.Frame):
	def __init__(self, master, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)
		self.master = master
		
		self.hacer_boton()
		self.boton.pack()

	def hacer_boton(self):
		self.boton =  tk.Button(self, text='Mensaje secreto', 
			command=self.siguiente, font=fuente_universal)

	def siguiente(self):
		Ventana2(self.master).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
		self.destroy()

class Ventana2(tk.Frame):
	def __init__(self, master, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)
		self.master = master

		self.hacer_cartel()
		self.cartel.pack()

		self.hacer_espacios_pass()
		self.lugar_pass.pack()
		self.ya_fallaron1 = False #Cuante si ya fallaron o no

		self.hacer_boton()
		self.boton.pack()

		self.hacer_advertencia()
		self.advertencia.pack()

	def hacer_cartel(self):
		self.cartel = tk.Label(self, font=fuente_universal,
			text='Introduzcan la clave. Tienen un único intento.')

	def hacer_boton(self):
		self.boton = tk.Button(self, text='Ingresar', 
			command=self.chequear, font=fuente_universal)

	def hacer_advertencia(self):
		self.var_advertencia = tk.StringVar()
		self.var_advertencia.set('')
		self.advertencia = tk.Label(self, textvariable=self.var_advertencia,
			font=fuente_universal, fg='red')

	def hacer_espacios_pass(self):
		self.pass_vars = [VarPass(tipo) for tipo in ('num', 'num', 'char')]

		f = tk.Frame(self)
		self.lugar_pass = f #el frame que incluye todos los espacios

		e = self.un_espacio(f, self.pass_vars[0])
		e.focus() #el cursor arranca acá
		e.pack(side=tk.LEFT)
		tk.Label(master=f, text=' - ', font=fuente_universal).pack(side=tk.LEFT)
		self.un_espacio(f, self.pass_vars[1]).pack(side=tk.LEFT)
		tk.Label(master=f, text=' , ', font=fuente_universal).pack(side=tk.LEFT)
		self.un_espacio(f, self.pass_vars[2]).pack(side=tk.LEFT)

	def un_espacio(self, master, pass_var): 
		#crea un espacion del ancho correcto con la variable asociada
		e = tk.Entry(master=master, width=2, textvariable=pass_var, font=fuente_universal)
		e.bind('<Return>', self.chequear) #para que apretar enter sea como apretar el botón
		return e

	def validar(self):
		codigos = (
			('15', '40', 'rg'),
			('15', '40', 'rg'),
			('15', '40', 'ab'), #este es uno extra de muestra
			)
		validar_este = lambda codigo: all(
			(v.get().lower()==val for v, val in zip(self.pass_vars, codigo)))
		return any((validar_este(c) for c in codigos))


	def chequear(self, *args):
		#si alguno está vacío, no lo acepta
		if any((v.get()=='' for v in self.pass_vars)):
			return 

		#pregunta si están seguros
		if not messagebox.askokcancel('¿Seguros?', '¿Están seguros de que esa es la respuesta correcta?'):
			return

		if self.validar():
			Ventana3(self.master).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
			self.destroy()
		else:
			if self.ya_fallaron1:
				Ventana3(self.master, exito=False).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
				self.destroy()
				return

			msg = 'La respuesta era incorrecta. Vamos con una segunda oportunidad, pero no una tercera.'
			messagebox.showwarning('Incorrecto', msg)
			self.var_advertencia.set('Les queda 1 intento')
			self.ya_fallaron1 = True

class Ventana3(tk.Frame):
	def __init__(self, master, exito=True, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)
		self.master = master
		
		self.mensaje(exito)
		self.hacer_cartel()
		self.cartel.pack()

	def mensaje(self, exito):
		msg1 = 'felicitaciones lograron salir de sala y el mensaje final de la ciencia es'
		msg2 = 'Fallaron'
		self.msg = msg1 if exito else msg2

	def hacer_cartel(self):
		self.cartel =  tk.Label(self, text=self.msg, font=fuente_universal)

class VarPass(tk.StringVar):
	def __init__(self, tipo):
		tk.StringVar.__init__(self)
		checker = self.checkear_num if tipo=='num' else self.checkear_char
		self.trace('w', checker)

	def cortar_long(self, longitud): #para que enren dos caracteres máximo
		if len(self.get()) > longitud:
			self.set(self.get()[:longitud])

	def checkear_num(self, *a):
		self.cortar_long(2) #no deja que haya más de dos caracteres
		if not self.get().isdigit():
			self.set(''.join((c for c in self.get() if c.isdigit())))

	def checkear_char(self, *a):
		self.cortar_long(2) #no deja que haya más de dos caracteres
		if not self.get().isalpha():
			self.set(''.join((c for c in self.get() if c.ischar())))

root = tk.Tk()
root.attributes('-fullscreen', True) #pantlla completa
#root.protocol("WM_DELETE_WINDOW", lambda: None) #Para que no se pueda salir con Alt+F4

Ventana1(root).place(relx=0.5, rely=0.5, anchor=tk.CENTER) #poner en el centro
root.mainloop()