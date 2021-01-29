
#Recibe el archivo orginal y una lista con las opciones
def indice(excel, archivo):
    fraccion = []
    for i in range(len(archivo)):
        fraccion.append(excel/archivo[i])
    return archivo[fraccion.index(max(fraccion))]

prueba = [1, 2, 3, 4, 0.5]

indice(2, prueba)







