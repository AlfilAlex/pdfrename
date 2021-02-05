import pandas as pd
import os
from os import walk
import shutil
import re
from tkinter import Tk 
from tkinter.filedialog import askdirectory, askopenfilename

#Creo clase y en init deben estar mypath, filenames y df
class incay_facturas():
    def __init__(self):
        self.mypath = None
        self.filenames = None
        self.new_folder = None
        self.df_interes = None
        self.nombre_excel = None
        self.hiperlinks = []
        self.parecido = []
    
    def mypath_func(self):
        Tk().withdraw() # que no aparezca la ventana
        path = askdirectory() # regresa la ruta
        (_, _, filenames) = next(walk(path))    #Se obtiene le nombre de cualquier archivo o carpeta
        filenames = [x.split('.')[0] for x in filenames if '.pdf' in x or '.PDF' in x] 
        self.mypath = str(path)
        self.filenames = filenames
        self.nombre_excel = str(self.mypath.split('/')[-1])
        self.new_folder = self.nombre_excel + '_renombrados'
       
    def dataframe(self):
        ruta_excel_original = askopenfilename() 
        self.df_interes = pd.read_excel(ruta_excel_original, 
                                    sheet_name = self.nombre_excel, #Si primero busca el excel, saltará un error
                                    header=5, 
                                    usecols='A:F',
                                    index_col=0).dropna(axis=0, how='all')

    def iniciador(self):
        self.comparador()
        
    def crear_carpeta(self, ruta):
        ruta_nueva = os.path.join(ruta, self.new_folder)
        os.mkdir(ruta_nueva)

    #crea un nombre y crea un archivo en una ruta nueva con el nombre
    #Despues lo manda a la función que crea una nueva columna
    def cambiarnombre(self, i, elemento, archivo, esta=True):
        if esta:
            nombre = str(i) + '-' + str(archivo) + '.pdf'
            nuevo_nombre = self.mypath + '/' +str(self.new_folder) + '/' + nombre    #ruta y nombre del documento nuevo
            try:
                antiguo_archivo = self.mypath + '/' + str(archivo) + '.pdf' # ruta y nombre del doc antiguo
                shutil.copy2(antiguo_archivo, nuevo_nombre)
                self.nuevacolumna(nuevo_nombre, elemento) 
            except:
                antiguo_archivo = self.mypath + '/' + str(archivo) + '.PDF'
                shutil.copy2(antiguo_archivo, nuevo_nombre)
                self.nuevacolumna(nuevo_nombre, elemento) 
        else:
            self.nuevacolumna('no_hay', elemento, esta=False) 
            
    #Crea una nueva columna con los hyperlinks    
    def nuevacolumna(self, path, elemento, esta=True):
        if esta:
            self.hiperlinks.append('=HYPERLINK("'+path+'","'+str(elemento)+'")')
        else:
            self.hiperlinks.append(elemento)
            
    #Recorre y compara los nombres de los excel y los nombres de los pdf en la carpeta
    def comparador(self):
        i = 0
        for elemento in self.df_interes['FACTURA']: 
            bandera = False

            if i ==0:
                self.crear_carpeta(self.mypath)

            if i % int(len(self.df_interes['FACTURA'])/100) == 0:
                self.avance(i)

            for archivo in self.filenames:   #Tiene los nombres de los archivos en carpeta        
                string = str(archivo) + '$'

                if re.findall(string.replace('-', ''), str(elemento).replace('-', '')):     #Elemento: del excel     #archivo: de la carpeta
                    i +=1            
                    self.cambiarnombre(i, str(elemento), archivo)
                    bandera = True
                    break 

            if bandera == False:
                i +=1
                self.cambiarnombre('no_hay', elemento, archivo, esta=False)
        self.volcado()
    
    def avance(self, i):
        os.system('clear')
        if i <= 100:
            print('Avance: '+ i*'|' + str(i) + '%')               
        elif i == len(self.df_interes['FACTURA']): 
            print('Avance: '+ 100*'|' + str(100) + '%')

    def volcado(self):
        nombre_final = self.mypath + '/' +str(self.new_folder) + '/' +self.nombre_excel + '_hiperb.xlsx'
        self.df_interes['Hypervinculos'] = self.hiperlinks
        self.df_interes.to_excel(nombre_final)











