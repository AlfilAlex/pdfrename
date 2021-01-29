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
        self.mypath = 'None'
        self.filenames = 'None'
        self.df_interes = 'None'
        self.nombre_e = 'None'
        self.hiperlins = []
        self.folder_newname = 'None'
        self.parecido = []
    
    def mypath_func(self):
        Tk().withdraw() # que no aparezca la ventana
        path = askdirectory() # regresa la ruta
        (_, _, filenames) = next(walk(path))             #Se obtiene le nombre de cualquier archivo o carpeta
        filenames = [x.split('.')[0] for x in filenames if '.pdf' in x or '.PDF' in x]        #Seleccion de pdfs
        self.mypath = str(path)
        self.filenames = filenames
        self.nombre_e = str(self.mypath.split('/')[-1])
        self.folder_newname = self.nombre_e + '_renombrados'

    def dataframe(self):
        ruta_excel_original = askopenfilename() 
        df_interes = pd.read_excel(ruta_excel_original, 
                                    sheet_name = self.nombre_e, #Si primero busca el excel, saltará un error
                                    header=5, 
                                    usecols='A:F',
                                    index_col=0).dropna(axis=0, how='all')
        self.df_interes = df_interes

    def iniciador(self):
        self.comparador(self.df_interes, self.filenames, self.mypath)
        
    def crear_carpeta(self, ruta):
        ruta_nueva = os.path.join(ruta, self.folder_newname)
        os.mkdir(ruta_nueva)

    #crea un nombre y crea un archivo en una ruta nueva con el nombre
    #Despues lo manda a la función que crea una nueva columna
    def cambiarnombre(self, i, elemento, archivo, ruta, esta=True):

        if esta:
            self.parecido.append((elemento, archivo))
            nombre = str(i) + '-' + str(archivo) + '.pdf'
            nuevo_nombre = ruta + '/' +str(self.folder_newname) + '/' + nombre    #ruta y nombre del documento nuevo
            try:
                antiguo_archivo = ruta + '/' + str(archivo) + '.pdf' # ruta y nombre del doc antiguo
                shutil.copy2(antiguo_archivo, nuevo_nombre)
                self.nuevacolumna(nuevo_nombre, elemento) #mandalo a nueva columna
            except:
                antiguo_archivo = ruta + '/' + str(archivo) + '.PDF'
                shutil.copy2(antiguo_archivo, nuevo_nombre)
                self.nuevacolumna(nuevo_nombre, elemento) #mandalo a nueva columna    
        else:
            self.parecido.append((elemento, '<- No esta el pdf'))
            self.nuevacolumna('nohay', elemento, esta=False) #mandalo a nueva columna
            
    #Crea una nueva columna con los hyperlinks    
    def nuevacolumna(self, path, elemento, esta=True):
        if esta:
            self.hiperlins.append('=HYPERLINK("'+path+'","'+str(elemento)+'")')
        else:
            self.hiperlins.append(elemento)
            
    #Recorre y compara los nombres de los excel y los nombres de los pdf en la carpeta
    def comparador(self, df_interes, filenames, mypath):
        i = 0
        control = 0
        for elemento in df_interes['FACTURA']: #df_interes['FACTURA'] tiene lo del excel
            bandera = False

            if i ==0:
                self.crear_carpeta(mypath)

            if i % int(len(df_interes)/100) == 0:
                os.system('clear')
                control += 1

                if control <= 100:
                    print('Avance: '+ control*'|' + str(control) + '%')               
                else: 
                    print('Avance: '+ 100*'|' + str(100) + '%')
                    
            for archivo in filenames:               #Tiene los nombres de los archivos en carpeta        
                string = str(archivo) + '$'   
                
                if re.findall(string.replace('-', ''), str(elemento).replace('-', '')):            #Elemento: del excel     #archivo: de la carpeta
                    i +=1            
                    self.cambiarnombre(i, str(elemento), archivo, mypath)
                    bandera = True
                    print(archivo, elemento)
                    break
                    
            if bandera == False:
                i +=1
                self.cambiarnombre('nohay', elemento, archivo, mypath, esta=False)
            #print(i, elemento)
        self.volcado()

    def volcado(self):
        nombre_final = self.mypath + '/' +str(self.folder_newname) + '/' +self.nombre_e + '_hiperb.xlsx'
        self.df_interes['Hypervinculos'] = self.hiperlins
        self.df_interes.to_excel(nombre_final)
        for elemento in self.parecido:
            print(elemento)

    #def comparador(self):
        #print(self.parecido)
        
