import pandas as pd
import os
from os import walk
import shutil
import re
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askdirectory, askopenfilename



Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
mypath = askdirectory() # show an "Open" dialog box and return the path to the selected file
(_, _, filenames) = next(walk(mypath))             #Se obtiene le nombre de cualquier archivo o carpeta
filenames = [x.split('.')[0] for x in filenames if '.pdf' in x or '.PDF' in x]        #Seleccion de pdfs


ruta_excel_original = askopenfilename() 
df_interes = pd.read_excel(ruta_excel_original, sheet_name = 'Sheet1')


#Nombre de la carpeta = Destino

folder_newname = 'destino'
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
hiperlins = []
def nuevacolumna(path, elemento, esta=True):
    if esta:
        hiperlins.append('=HYPERLINK("'+path+'","'+str(elemento)+'")')
    else:
        hiperlins.append(elemento)


        
#Recorre y compara los nombres de los excel y los nombres de los pdf en la carpeta

def iniciador(data_excel, filenames, ruta):

    i = 0
    control = 0
    for elemento in data_excel['FACTURA']:
        bandera = False                                        #df_interes['FACTURA'] tiene lo del excel
        if i ==0:
            crear_carpeta(ruta)
        
        if i % int(len(data_excel)/100) == 0:
            os.system('clear')
            control += 1
            if control <= 100:
                print('Avance: '+ control*'|' + str(control) + '%')                
            else: 
                print('Avance: '+ 100*'|' + str(100) + '%')
                

        for archivo in filenames:               #Tiene los nombres de los archivos en carpeta        
            string = str(archivo) + '$'   
            
            if re.findall(string, str(elemento)):            #Elemento: del excel     #archivo: de la carpeta
                i +=1            
                cambiarnombre(i, str(elemento), archivo, ruta)
                bandera = True
                break
                
        if bandera == False:
            i +=1
            cambiarnombre('nohay', elemento, archivo, ruta, esta=False)
            

iniciador(df_interes, filenames, mypath)

df_interes['Hypervinculos'] = hiperlins
df_interes.to_excel('intento3.xlsx')

