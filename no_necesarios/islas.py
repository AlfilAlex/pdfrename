#%%
import pandas as pd

class islas:
    def __init__(self, pajaros, nodos, nombre):
        self.pajaros = pajaros
        self.nodos = nodos
        self.nombre = nombre

    def pajaros_isla(self):
        return self.pajaros
    def nodos_isla(self):
        return self.nodos
    def nombre_isla(self):
        return self.nombre

    def pajaros_emigracion(self, cantidad):
        self.pajaros = self.pajaros - cantidad  
    def pajaros_migracion(self, cantidad):
        self.pajaros = self.pajaros + cantidad
    def pajaros_emigracion(self, cantidad):
        self.pajaros = self.pajaros - cantidad        

#%%
isla_A = islas(1100, {'A-B': 0.001, 'A-C': 0.01, 'A-F': 0.01}, 'A')
isla_B = islas(100, {'B-C': 0.01, 'B-A': 0.06}, 'B')
isla_C = islas(100, {'C-A': 0.001, 'C-B': 0.01, 'C-E': 0.01}, 'C')
isla_D = islas(200, {'D-A': 0.01, 'D-A': 0.04}, 'D')
isla_E = islas(100, {'E-A': 0.001, 'E-F': 0.01, 'E-D': 0.021}, 'E')
isla_F = islas(100, {'F-D': 0.01, 'F-B': 0.01, 'F-C': 0.01}, 'F')
lista_islas = [isla_A, isla_B, isla_C, isla_D, isla_E, isla_F]

dic_islas = {}

for isla in lista_islas:
    dic_islas[isla.nombre_isla()] = []

for i in range(10000):
    for isla in lista_islas:
        nodo = isla.nodos_isla()
        #Generamos una lista con las islas complementarias a 'isla'
        nombres = [nombre for nombre in lista_islas if nombre != isla]
        for nombre in nombres:
            nodo = isla.nombre_isla() + '-' + nombre.nombre_isla()

            try:
                cantidad = isla.nodos_isla()[nodo]* isla.pajaros_isla()
            except:
                continue

            isla.pajaros_emigracion(cantidad)
            nombre.pajaros_migracion(cantidad)

        if isla == isla_A:
            dic_islas[isla.nombre_isla()].append(isla.pajaros_isla())
            #print(isla.pajaros_isla())

        if isla == isla_B:
            dic_islas[isla.nombre_isla()].append(isla.pajaros_isla())
            #print(isla.pajaros_isla())

        if isla == isla_C:
            dic_islas[isla.nombre_isla()].append(isla.pajaros_isla())
            #print(isla.pajaros_isla())

        if isla == isla_D:
            dic_islas[isla.nombre_isla()].append(isla.pajaros_isla())
            #print(isla.pajaros_isla())

        if isla == isla_E:
            dic_islas[isla.nombre_isla()].append(isla.pajaros_isla())
            #print(isla.pajaros_isla())

        if isla == isla_F:
            dic_islas[isla.nombre_isla()].append(isla.pajaros_isla())
            #print(isla.pajaros_isla())

df = pd.DataFrame(dic_islas)
df.plot()
print(df)















# %%
