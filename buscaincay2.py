import pandas as pd
from os import walk, path, mkdir
from shutil import copy2
from tkinter import Tk 
from tkinter.filedialog import askdirectory, askopenfilename
from nltk import edit_distance

#Creo clase y en init deben estar mypath, filenames y df
class incay_facturas():

    """ Esta clase tiene los metodos necesarios para comparar el nombre de los archivos
        PDF de una carpeta con los nombres de una columna de un archivo CSV o XLSX (con nombres 
        parecidos a los de los PDFs). Posteriormente hace una copia de los archivos con el nombre
        correspondiente al CSV o XLSX en una nueva carpeta. Por ultimo genera un Excel con
        las asignaciones correspondientes y una columna con un hypervinculo hacia el nuevo
        archivo renombrado
    """

    def __init__(self):
        self.mypath = None
        self.filenames = None
        self.new_folder = None
        self.df_interes = None
        self.nombre_excel = None
        self.hiperlinks = []
        self.parecido = []

    def iniciador(self):
        self.comparador()
        return self.hiperlinks

    def comparador(self):

        """ Compara los nombres encontrados en la columna Factura del excel
            con el nombre de los archivos en la carpeta. Busca el mejor resultado
            del edit distance y lo pasa ambos nombres a la función cambiar nombre
            en donde será procesado para crear un archivo y una fila.
        """
        
        i = 0
        if i == 0:
            self.crear_carpeta(self.mypath)

        for celda_excel in self.df_interes['FACTURA']: 
            
            celda_excel = str(celda_excel)
            bandera = False
            best_result = (100, 'archivo') #will save the best result

            for archivo in self.filenames:   #File names in the folder        
                
                nombre_archivo = archivo.lstrip('0').replace('-', '')
                elemento_excel = str(celda_excel).lstrip('0').replace('-', '')
                num_diff_char = edit_distance(nombre_archivo, elemento_excel)

                if num_diff_char == 0:
                    i +=1            
                    self.cambiarnombre(i, celda_excel, archivo)
                    bandera = True
                    break
                else:
                    if num_diff_char < best_result[0]:
                        best_result = (num_diff_char, archivo)

            # Si no se encontró el archivo (bandera == False) se busca el mejor resultado
            # si el mejor resultado tuvo un edit distance mayor a 3, se toma 
            # como un archivo no encontrado.
            if not bandera and best_result[0] <= 3:
                i +=1
                self.cambiarnombre(i, celda_excel, best_result[1])
            elif not bandera:
                i +=1 
                self.cambiarnombre('no_hay', celda_excel, nombre_archivo, esta = False)
                           
        self.volcado()


    def crear_carpeta(self, ruta):
        ruta_nueva = path.join(ruta, self.new_folder)
        mkdir(ruta_nueva)


    def cambiarnombre(self, i, celda_excel, archivo, esta = True):

        """ Crea un nombre y un archivo en una ruta nueva.
            Despues lo manda a la función que crea una nueva columna
        """

        if esta:
            nombre = str(i) + '-' + str(archivo) + '.pdf'
            nuevo_nombre = self.mypath + '/' +str(self.new_folder) + '/' + nombre    #ruta y nombre del documento nuevo
            oldfile_name = str(archivo)
            try:
                antiguo_archivo = self.mypath + '/' + oldfile_name + '.pdf' # ruta y nombre del doc antiguo
                copy2(antiguo_archivo, nuevo_nombre) 
                self.nuevacolumna(nuevo_nombre, celda_excel) 
            except:
                self.nuevacolumna('no_hay', celda_excel, esta = False)
        else:
            self.nuevacolumna('no_hay', celda_excel, esta = False) 


    def mypath_func(self):
        
        """Define donde se encuentra la carpeta con los PDFs y guarda los nombres de estos
        archivos. Por ultimo crea una carpeta donde guardará los nuevos archivos renombrados
        """

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


    # Crea una nueva columna con los hyperlinks    
    def nuevacolumna(self, path, elemento, esta=True):
        """ Si el elemento se encuentra, entonces se crea su hipervinculo y se crea su correspondiente fila.
            Pero si no está, entonces solo sea grega el elemento, con la finalidad de no dejar la celda vacia
        """
        if esta:
            self.hiperlinks.append('=HYPERLINK("'+path+'","'+str(elemento)+'")')
        else:
            self.hiperlinks.append(elemento)
            

    def volcado(self):
        nombre_final = self.mypath + '/' +str(self.new_folder) + '/' +self.nombre_excel + '_hiperb.xlsx'
        self.df_interes['Hypervinculos'] = self.hiperlinks
        self.df_interes.to_excel(nombre_final)






