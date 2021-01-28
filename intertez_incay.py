from tkinter import *
#from buscaincay2 import carpeta_madre



root = Tk()
root.geometry('400x300')




frame = Frame(root, width=400, height=250)
frame.grid(row=0, column=0)


boton_carpeta = Button(frame, text='Buscar carpeta')
boton_carpeta.grid(row=0, column = 0, padx=20, pady=30)


boton_archivo = Button(frame, text='Buscar excel')
boton_archivo.grid(row=1, column=0, padx=20, pady=30)

boton_iniciar = Button(frame, text='Iniciar proceso')
boton_iniciar.grid(row=2, column=0, pady=30, columnspan=2)


root.mainloop()