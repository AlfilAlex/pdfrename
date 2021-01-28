from tkinter import *
from buscaincay2 import incay_facturas
#from buscaincay2 import carpeta_madre



root = Tk()
root.geometry('170x300')

facturas = incay_facturas()



def buscacarpeta():
    facturas.mypath_func()
def buscaexcel():
    facturas.dataframe()
def inicia_programa():
    facturas.iniciador()    



frame = Frame(root, width=400, height=250)
frame.grid(row=0, column=0)


boton_carpeta = Button(frame, text='Buscar carpeta', command=buscacarpeta)
boton_carpeta.grid(row=0, column = 0, padx=20, pady=30)


boton_archivo = Button(frame, text='Buscar excel', command=buscaexcel)
boton_archivo.grid(row=1, column=0, padx=20, pady=30)

boton_iniciar = Button(frame, text='Iniciar proceso', command=inicia_programa)
boton_iniciar.grid(row=2, column=0, pady=30, columnspan=2)


root.mainloop()
