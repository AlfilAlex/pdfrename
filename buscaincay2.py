import pandas as pd
import os
from os import walk
import shutil
import re
from tkinter import Tk 
from tkinter.filedialog import askdirectory, askopenfilename

#Creo clase y en init deben estar mypath, filenames y df
class iniciador():
    def __init__():
        self.mypath = None
        self.filenames = None
        self.df_interes = None

        #Aun estoy viendo qué onda
        nombre_final = nombre_e + '_hiperb.xlsx'
        folder_newname = 'nombre_e' + '_renombrados'
        hiperlins = []



    def mypath():
        Tk().withdraw() # que no aparezca la ventana
        mypath = askdirectory() # regresa la ruta
        (_, _, filenames) = next(walk(mypath))             #Se obtiene le nombre de cualquier archivo o carpeta
        filenames = [x.split('.')[0] for x in filenames if '.pdf' in x or '.PDF' in x]        #Seleccion de pdfs
        self.mypath = mypath
        self.filenames = filenames
        nombre_e = str(mypath.split('/')[-1])

    def dataframe():
        ruta_excel_original = askopenfilename() 
        df_interes = pd.read_excel(ruta_excel_original, 
                                    sheet_name = nombre_e, 
                                    header=5, 
                                    usecols='A:F',
                                    index_col=0).dropna(axis=0, how='all')
        self.df_interes = df_interes
        

    #Nombre de la carpeta = Destino
    #folder_newname = 'nombre_e' + '_renombrados'
    def crear_carpeta(ruta):
        ruta_nueva = os.path.join(ruta, folder_newname)
        os.mkdir(ruta_nueva)
        #print('Se creo una nueva carpeta destino')


    #crea un nombre y crea un archivo en una ruta nueva con el nombre
    #Despues lo manda a la función que crea una nueva columna
    def cambiarnombre(i, elemento, archivo, ruta, esta=True):
        if esta:
            nombre = str(i) + '-' + str(archivo) + '.pdf'
            nuevo_nombre = ruta + '/destino/' + nombre    #ruta y nombre del documento nuevo
            try:
                antiguo_archivo = ruta + '/' + str(archivo) + '.pdf' # ruta y nombre del doc antiguo
                shutil.copy2(antiguo_archivo, nuevo_nombre)
                nuevacolumna(nuevo_nombre, elemento) #mandalo a nueva columna
            except:
                antiguo_archivo = ruta + '/' + str(archivo) + '.PDF'
                shutil.copy2(antiguo_archivo, nuevo_nombre)
                nuevacolumna(nuevo_nombre, elemento) #mandalo a nueva columna    
        else:
            nuevacolumna('nohay', elemento, esta=False) #mandalo a nueva columna
            
    #Crea una nueva columna con los hyperlinks    
    #hiperlins = []
    def nuevacolumna(path, elemento, esta=True):
        if esta:
            hiperlins.append('=HYPERLINK("'+path+'","'+str(elemento)+'")')
        else:
            hiperlins.append(elemento)
            
    #Recorre y compara los nombres de los excel y los nombres de los pdf en la carpeta
    def iniciador(df_interes, filenames, mypath):
        i = 0
        control = 0
        for elemento in df_interes['FACTURA']: #df_interes['FACTURA'] tiene lo del excel
            bandera = False

            if i ==0:
                crear_carpeta(mypath)

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
                    cambiarnombre(i, str(elemento), archivo, mypath)
                    bandera = True
                    print(archivo, elemento)
                    break
                    
            if bandera == False:
                i +=1
                cambiarnombre('nohay', elemento, archivo, mypath, esta=False)
            print(i, elemento)

#iniciador(df_interes, filenames, mypath)
#nombre_final = nombre_e + '_hiperb.xlsx'
#df_interes['Hypervinculos'] = hiperlins
#df_interes.to_excel(nombre_final)

