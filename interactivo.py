# -- coding: utf-8 --
"""
Created on Sat Jun  8 00:37:29 2019

@author: Marcos
"""

#sr, duration, freq = 32000, 10, 280
#time = np.linspace(0, duration, duration * sr, endpoint=False)
#seno = (2**15-1) * np.sin(time * 2 * np.pi * freq) / 4
#seno = seno.astype(np.int16)
#
#ply_this = sa.play_buffer(seno, 1, 2, sr)
#ply_this.wait_done()

#%%
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from itertools import chain
import simpleaudio as sa

valores_que_cambian = {'fs':44100, #en Hz
                       'duracion':1, #en seg
                       'frec':150, #en Hz
                       'volumen':80 #en %
                       } #incluye los defauls
defaults = dict(show_discreto='0', pers_shown=1, **valores_que_cambian)
fs_permitidas = (8, 11.025, 16, 22.05, 32, 44.1, 48, 88.2, 96, 192) #kHz

class Plot(Figure):
    
    def __setattr__(self, name, value):
        '''Me aseguro de que cuando uno de los valores de la curva cambie,
        self.changed también cambie.'''
        super().__setattr__(name, value)
        if name in valores_que_cambian:
            self.changed = True
            if hasattr(self, 'show_discreto') and self.show_discreto:
                self.update()
               
    def __init__(self, vars_amp, vars_fas, fs=None, duracion=None, frec=None, volumen=None, *a, **k):
        
        #variables de la curva
        self.amplis = vars_amp
        self.fases = vars_fas
               
        #parámetros del sonido
        self.reset_params()

        super().__init__(*a, **k)
        self.reset_mode() #poner los valores iniciales
        self.init_plot() 

        self.personalizado_init = False

    @property
    def frec(self):
        return self._frec
    @frec.setter
    def frec(self, value):
        self._frec = value
        self.update_label()

    @property
    def show_discreto(self):
        return self._show_discreto
    @show_discreto.setter
    def show_discreto(self, value):
        self._show_discreto = bool(value)
        self.discreta.set_visible(self.show_discreto)
        self.update()
        
    def _make_discreta(self):
        '''Plotea la curva discreta. Crea el vector de tiempo y la línea correspondientes.'''
        self.t_discreto = self._make_t_discreto()
        
        #intento borrar la anterior
        try:
            self.discreta.remove()
        except (ValueError, AttributeError):
            pass                
        
        self.discreta = self.axes[1].plot(self.t_discreto/self.t_discreto[-1], 
                                 self.senos(self.t_discreto),
                                 '--', color='C1')[0]
        self.discreta.set_visible(self.show_discreto)

    @property
    def pers_shown(self):
        return self._pers_shown
    @pers_shown.setter
    def pers_shown(self, value):
        value = int(np.clip(value, 1, 10)) #entro 0 y 10
        self._pers_shown = value
        #acualizo vectores de tiempo
        self.t = np.linspace(0, self.pers_shown, 800)
        self.t_discreto = self._make_t_discreto()
        
        self.update()
        
    def _make_t_discreto(self):
        '''Crea el vector de tiempo para la onda discreta.'''
        puntos = round(self.pers_shown * self.fs / self.frec)
        if puntos>=800:
            return self.t #no más puntos que t
        else:
            puntos = max(puntos, 2)
            return np.linspace(0, self.pers_shown, puntos)

    def init_plot(self):
        '''Inicializa la fig con los dos plots. Linquea la modificación de los 
        valores de los parámetros a ala actualización del plot.''' 
        self.subplots(1,2)
        self.barras()
        self.curva()
        for v in chain(self.amplis, self.fases):
            v.trace('w', self.update)

    def put_canvas(self, master, mode='grid', *args, **kwargs):
        '''Pone la imagen en la ventana.'''
        self.my_canvas = FigureCanvasTkAgg(self, master=master)

        if mode.lower()=='grid':
            self.my_canvas.get_tk_widget().grid(*args, **kwargs)
        elif mode.lower()=='pack':
            self.my_canvas.get_tk_widget().pack(*args, **kwargs)
        elif mode.lower()=='place':    
            self.my_canvas.get_tk_widget().place(*args, **kwargs)  
        else:
            raise ValueError("Mode must be 'grid', 'place', or 'pack'.") 
        self.my_canvas.draw()

    def barras(self):
        '''Gráfico de barras de las amplitudes.'''
        ax = self.axes[0]
        x = list(range(len(self.amplis)))
        y = [v.get() for v in self.amplis]
        self.bars = ax.bar(x,y)
        ax.set_xlabel('# Armónico')
        ax.set_ylabel('Amplitud [u.a.]')
        ax.set_ylim(0,105)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    def senos(self, t, frec=1):
        '''Genero la suma de senos normalizada.'''
        senito = lambda amp, fas, i: amp * np.sin(np.pi * 2 * (i+1) * t * frec + fas * 2 * np.pi / 360)
        senos = sum([senito(a.get(), f.get(), i) for i, (a,f) in enumerate(zip(self.amplis, self.fases))])
        if np.abs(senos).max==0:
            return np.zeros(senos.shape)
        else:
            return senos/np.abs(senos).max()

    def curva(self):
        '''Gráfico de la curva de un período del sonido.'''
        ax = self.axes[1]
        self.t = np.linspace(0, self.pers_shown, 800)      
        self.l = ax.plot(self.t, self.senos(self.t))[0] #el [0] para tomar la línea del plot
        self._make_discreta()
        
#        ax.set_xticks([],[]) #sin ticks en los ejes
        ax.set_yticks([],[]) #sin ticks en los ejes
        self.update_label()
        
    def update_label(self):
        try:
            self.axes[1].set_xlabel('Período [aprox. {:.2f}ms]'.format(
                    1000 * self.pers_shown/self.frec))
        except AttributeError:
            pass
        
    def update(self, *a): #mejorar tomando índice cambiado (acelerar)
        '''Actualizo gráficos.'''
        #Las barras:
        try: 
            for b, v in zip(self.bars, self.amplis):
                b.set_height(v.get())
            #Los senos:
            self.l.set_ydata(self.senos(self.t))
            self.update_label()
            if self.show_discreto: #solo actualizo si la estoy mostrando
                if self.changed: #si cambiaron fs o frec, grafico de cero
                    self._make_discreta()
                else:
                    self.discreta.set_ydata(self.senos(self.t_discreto))
            #Muestro lo nuevo
            self.my_canvas.draw()
            self.changed = True
        except AttributeError:
            pass
        
    def reset_mode(self):
        '''Reinicio todos los valores de amplitudes y fases.'''
        for v in chain(self.amplis[1:], self.fases):
            v.set(0)
        self.amplis[0].set(100)
        self.changed = True
        
    def reset_params(self):
        '''Reinicio todos los valores de los parámetros.'''
        
        ### HAY QUE MODIFICAR LAS VARIABLES!!!
        
        #parametros del sonido
        for k, v in valores_que_cambian.items():
            setattr(self, k, v)
            
        #parametros del gráfico
        self._show_discreto = False
        self.pers_shown = 1
        
        self.update()

        
    def create_sound(self):
        '''Crea el sonido a reproducir, sólo si hubo cambios desde la última vez.'''
        if self.changed:
            tiempo = np.linspace(0, self.duracion, self.duracion * self.fs, endpoint=False)

            # Una envolvernte para que arranque y termine con 0.05 segundos de control de volumen
            seno_env = np.sin(np.linspace(-np.pi/2, np.pi/2, 0.05 * self.fs)) * .5
            envolvente = np.concatenate((.5 + seno_env, np.ones(len(tiempo)-2*len(seno_env)), .5-seno_env))      
            
            self.sound = self.volumen/100 * (2**15-1) * self.senos(tiempo, self.frec)
            self.sound *= envolvente
            self.sound = self.sound.astype(np.int16)

            self.changed = False
        return self.sound
    
    def play(self):
        self.player = sa.play_buffer(self.create_sound(), 1, 2, self.fs)
        
    def stop(self):
        if hasattr(self, 'player'):
            self.player.stop()
    
    def call_or_place(self, new, old):
        '''Reemplaza los valores en old por los dados en new, que puede ser un
        iterable (no un generador!), o un callable que cree los nuevos valores.'''
        if callable(new):
            for i, o in enumerate(old):
                o.set(new(i+1))
        else:
            if len(old)>len(new):
                new += [0] * (len(old)-len(new))
            for o, n in zip(old, new):
                o.set(n)
    
    def set_mode(self, amplitudes, fases=[]):
        self.call_or_place(amplitudes, self.amplis)
        self.call_or_place(fases, self.fases)


#=====================================
###### Defino modos preseteados#######
#=====================================

def no_implementado():
    messagebox.showinfo(title='No implementado', message='Regrese más tarde')

def random():
    func = lambda i: np.random.randint(0,100)
    p.set_mode(func, func)

def cuadrada():
    def amplis_func(i):
        if i%2: #sólo los impares
            return 100/i #amplitud máxima es 100...
        else:
            return 0
    p.set_mode(amplis_func)

def triangular():
    def amplis_func(i):
        if i%2: #sólo los impares
            return 100/(i**2) #amplitud máxima es 100...
        else:
            return 0
        
    def fases_func(i):
        i += 1
        if not (i+1)/2%2: #los de índice 3, 7, 11, 15, ...
            return 180
        else:
            return 0
    p.set_mode(amplis_func, fases_func)

def sawtooth():
    def amplis_func(i):
        return 100/i
        
    def fases_func(i):
        i += 1
        if not i%2: #los de índice 3, 7, 11, 15, ...
            return 180
        else:
            return 0
    p.set_mode(amplis_func, fases_func)

def violin():
    amps = [100, 83, 45, 23, 6, 25, 27, 6, 2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0]
    p.set_mode(amps)

def flauta():
    amps = [100, 19, 7, 10, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    p.set_mode(amps)

def corno():
    amps = [100, 16, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    p.set_mode(amps)

def organo():
    amps = [85, 69, 62, 20, 2, 25, 1, 100, 13, 3, 0, 67, 0, 0, 1, 25, 0, 6, 0, 2, 1]
    p.set_mode(amps)

def nada():
    pass

modos = {'Elija uno':nada,
         '  Cuadrada':cuadrada,
         '  Triangular':triangular,
         '  Sawtooth':sawtooth,
         '  Violín':violin,
         '  Flauta':flauta,
         '  Corno':corno,
         '  Órgano':organo
         }

nuevos_modos = {}

def switcher(*a):
    modos[cb.get()]()
  
    
#==========================================
###### Defino cosas para la interfaz#######
#==========================================

def makeslider(master, span, name, var):
    '''Crea un slider vertical con un título arriba y un spinbox abajo. El spinbox y el slider 
    están ligados al mism valor. Mete todo en un tk.Frame.
    Toma el padre de todo esto, el rango de valores, el nombre y la variable que modifican.'''
    frame = tk.Frame(master=master)
    tk.Label(master=frame, text=name).pack()
    tk.Scale(master=frame, from_=span[1], to=span[0], sliderlength=12, width=13, variable=var).pack()
    tk.Spinbox(master=frame, from_=span[0], to=span[1], width=3 , textvariable=var, wrap=True).pack()
    return frame


def makeone(master, name, ind):
    '''Crea un toolbar que con dos unidades creadas por makeslider que corresponden a amplitud
    y fase. Mete la dos en un tk.Frame y les da un nombre.
    Toma ek padre de todo esto, el nombre y el índice de la variable.'''
    toolbar = tk.Frame(master=master)
    
    titulo = tk.Frame(master=toolbar, relief=tk.RIDGE, padx=3, pady=2, borderwidth=1)
    tk.Label(master=titulo, text=name).pack(fill=tk.X)
    
    botones = tk.Frame(master=toolbar, relief=tk.RIDGE, padx=3, pady=2, borderwidth=1)
    makeslider(botones, (0,100), 'Ampli', vars_amp[ind]).pack(fill=tk.X)
    makeslider(botones, (0,360), 'Fase', vars_fas[ind]).pack(fill=tk.X)
    
    titulo.pack(fill=tk.X)
    botones.pack(fill=tk.X)
    return toolbar


def paramvar(paramname, dtype='int', default=0):
    '''Crea una tk.Variable y la asocia al atributo de Plot dado en paramname.
    El tipo de variable será el de dtype. La variable está inicializada en el
    valor actual del atributo correspondiente.'''
    if dtype=='int':
        var = tk.IntVar()
    elif dtype=='double':
        var = tk.DoubleVar()
    elif dtype=='str':
        var = tk.StringVar()
    elif dtype=='bool':
        var = tk.BooleanVar()
    else:
        raise ValueError(
                "dtype must be one of ('int', 'double', 'str', 'bool'), but was '{}'".format(dtype))
        
    #Intenta poner el valor existente como inicial. Si no hay pone cero
    var.set(getattr(p, paramname, default))
    var.trace('w', lambda *a: setattr(p, paramname, var.get()))
    return var
    

def makeparam(master, name, unit, variable, span=[0,100]):
    '''Crea un spinbox para la variable dada, le pone nombre y unidades.'''
    frame = tk.Frame(master=master)
    tk.Label(master=frame, text=name).grid(columnspan=2)
    tk.Spinbox(master=frame, textvariable=variable,
               from_=span[0], to=span[1], width=6).grid(row=1, column=0)
    tk.Label(master=frame, text=unit).grid(row=1, column=1)
    return frame


def play(boton):
    '''Desactiva el botón, lo matiene apretado y reproduce el sonido.'''
    boton.config(relief=tk.SUNKEN, state=tk.DISABLED)
    try:
        p.play()
    except ValueError:
        msg = ('Para reproducción del sonido, la frecuencia de sampleo debe ser una '
               'de las siguientes, en kHz: \n{}').format(str(fs_permitidas)[1:-1])
               
        messagebox.showwarning(title='Frecuencia inválida', message=msg)
    p.player_after_id = boton.after(int(p.duracion * 1000), lambda:levantar(boton))


def levantar(boton):
    '''Devuelve el botón al estado desclickeado y activo.'''
    boton.config(relief=tk.RAISED, state='normal')


def stop(boton):
    '''Cancela la reproducción dle sonido y rehabilita el botón.'''
    p.stop()
    levantar(boton)
    if hasattr(p, 'player_after_id'):
        boton.after_cancel(p.player_after_id)


def reset_params(variables_dictionary):
    for k, val in variables_dictionary.items():
        val.set(defaults[k])


def get_vals(name):
    return [int(v.get()) for v in getattr(p, name)]


def agregar(entry_wdgt):
    nuevo = entry_wdgt.get()
    if nuevo == '':
        messagebox.showwarning(title='Nombre faltante', message='Indique un nombre en el campo adecuado')
        return

    amps = get_vals('amplis')
    fas = get_vals('fases')

    nuevo = '   ' + nuevo
    nuevos_modos[nuevo] = (amps, fas)
    
    def setter(name):
        p.set_mode(*nuevos_modos[name])

    if not p.personalizado_init:
        modos['Personalizados'] = nada
        p.personalizado_init = True
        
    modos[nuevo] = lambda: setter(nuevo)

    cb['values'] = list(modos.keys())


def borrar():
    global modos
    global nuevos_modos
    
    nombre = cb.get()
    if nombre in nuevos_modos:
        cb.set('Elija uno')
        del modos[nombre]
        del nuevos_modos[nombre]
        cb['values'] = list(modos.keys())
    else:
        messagebox.showwarning(title='No permitido', message='Sólo puede eliminar opciones personalizadas no las preexistentes.')
    # print(nuevos_modos)
    # print(modos.keys())


#=============================
###### Creo la interfaz#######
#=============================

#La ventana grande
root = tk.Tk()
#root.geometry('350x200')

#Variables que van a tener las funciones y que los botones modifican
cant = 11 #cuántos armónicos uso?
vars_amp = [tk.DoubleVar() for _ in range(cant)]
vars_fas = [tk.DoubleVar() for _ in range(cant)]

#Pongo gráfico
p = Plot(vars_amp, vars_fas)
p.put_canvas(root, 'grid', row=0, column=0, columnspan=cant, sticky='ew')

#Hago botoneras de armónicos
nombres = ['Modo {}'.format(i) for i in range(cant)]
for i, n in enumerate(nombres):
    makeone(root, n, i).grid(row=1, column=i)

###Botonera de acciones###
botonera = tk.Frame(master=root)
botonera.grid(row=0, column=cant+1, rowspan=2, padx=10)

###Parámetros###
# La caja externa y las dos internas
botonera_params = tk.Frame(master=botonera, relief=tk.RIDGE, padx=3, pady=2, borderwidth=1)
botonera_params.pack(fill=tk.X, pady=10)
cont_1 = tk.Frame(botonera_params)
cont_1.pack(pady=10)
cont_2 = tk.Frame(botonera_params)
cont_2.pack(pady=10)

# Variables
nombres = ['frec', 'fs', 'pers_shown', 'show_discreto']
var_dict = {k:paramvar(k, default=defaults[k]) for k in nombres}
var_dict['duracion'] = paramvar('duracion', default=defaults['duracion'], dtype='double')

makeparam(cont_1, 'Frecuencia', 'Hz', var_dict['frec'], span=[0, 22000]).pack()
makeparam(cont_1, 'Duración', 'seg', var_dict['duracion'], span=[0,20]).pack()

makeparam(cont_2, 'Frecuencia\nde sampleo', 'Hz', var_dict['fs'], span=[0,44200]).pack()
makeparam(cont_2, 'Períodos', '  ', var_dict['pers_shown'], span=[1,10]).pack()

tk.Button(master=cont_2, text='Reiniciar', 
          command= lambda : reset_params(var_dict)).pack(pady=10)
tk.Checkbutton(cont_2, text='Mostrar discreta', variable=var_dict['show_discreto']).pack()

###Play###
# La caja externa
botonera_play = tk.Frame(master=botonera, relief=tk.RIDGE, padx=3, pady=2, borderwidth=1)
botonera_play.pack(fill=tk.X, pady=10)
contenedor = tk.Frame(master=botonera_play)
contenedor.pack(pady=5)

# Botón de play
tam = dict(height=1, width=1, padx=6) #parámetros de los botones
play_button = tk.Button(master=contenedor, text='⏵', **tam)
play_button.config(command=lambda:play(play_button))
play_button.grid(row=0, column=0, padx=2)

# Botón de stop
stop_button = tk.Button(master=contenedor, text='||', command=lambda:stop(play_button), **tam)
stop_button.grid(row=0, column=1, padx=2)

# Volúmen
makeslider(contenedor, (0,100), 'Volumen', paramvar('volumen')).grid(row=1, columnspan=2)

###Presets###
# La caja externa
botonera_presets = tk.Frame(master=botonera, relief=tk.RIDGE, padx=3, pady=2, borderwidth=1)
botonera_presets.pack(fill=tk.X, pady=10)

formato = dict(fill=tk.X, pady=10)

# Botones de aleatorio y reinicio
tk.Button(master=botonera_presets, text='¡Aleatorio!', command=random).pack(**formato)
tk.Button(master=botonera_presets, text='Reiniciar', command=p.reset_mode).pack(**formato)

#Menu de opciones
tk.Label(master=botonera_presets, text='Presets:').pack(fill=tk.X)
cb = ttk.Combobox(botonera_presets, state='readonly', values=list(modos.keys()), 
                  width=max([len(m) for m in modos.keys()]))
cb.bind("<<ComboboxSelected>>", switcher)
cb.set('Elija uno')
cb.pack(fill=tk.X)

#Botón de aplicar el modo seleccionado
tk.Button(master=botonera_presets, text='Borrar', command=borrar).pack(**formato)
tk.Button(master=botonera_presets, text='Reaplicar', command=switcher).pack(**formato)

tk.Label(master=botonera_presets, text='Nombre:').pack(fill=tk.X)
e = tk.Entry(master=botonera_presets)
e.pack(fill=tk.X)
tk.Button(master=botonera_presets, text='Agregar', command=lambda: agregar(e)).pack(**formato)


###Guardar###
# tk.Button(master=botonera, text='Guardar?', state=tk.DISABLED).pack(**formato)


root.mainloop()
