def indice_parecido(lista1, lista2):
    for i in lista1:
        parecidos = []                     
        for e in lista 2:
            if i in e:
                parecidos.append((i, e))
                
    lista_indi = []
    
    for elemento in parecidos:
        lista_indi.append(elemento[0]/elemento[1])
    indice = lista_indi.index(max(lista_indi))
    
    return parecidos[indice]
        
        
        
    
    

























