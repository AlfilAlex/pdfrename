#from tkinter import *
from tkinter import Tk, Frame, Button, Text, W, N, E
from buscaincay2 import incay_facturas
#from buscaincay2 import carpeta_madre

root = Tk()
#root.geometry('270x500')
root.title('Programa_INCAY')

facturas = incay_facturas()


def buscacarpeta():
    facturas.mypath_func()
def buscaexcel():
    facturas.dataframe()
def inicia_programa():
    lista = facturas.iniciador()
    for elemento in lista:
        cuadro_text.insert(END, ', '.join(elemento[0:2]) + '\n')    



frame = Frame(root)#, width=400, height=250)
frame.grid(row=0, column=0)


boton_carpeta = Button(frame, text='Buscar carpeta', command=buscacarpeta)
boton_carpeta.grid(row=0, column = 0, padx=20, pady=30)

boton_archivo = Button(frame, text='Buscar excel', command=buscaexcel)
boton_archivo.grid(row=1, column=0, padx=20, pady=30)

boton_iniciar = Button(frame, text='Iniciar proceso', command=inicia_programa)
boton_iniciar.grid(row=2, column=0, pady=30)

cerrar = Button(frame, text='Cerrar', command=root.destroy)
cerrar.grid(row=3, column=0, padx=20, pady=30)

Frame_2 = Frame(frame)
Frame_2.grid(row = 0, column = 1, rowspan = 4)


cuadro_text = Text(Frame_2)
cuadro_text.grid(row = 0, column = 0, rowspan = 4, sticky=E + N)
cuadro_text.grid_propagate(False)

root.mainloop()
