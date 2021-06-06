import pandas as pd 

df_incompleto = pd.read_excel('incompleto2.xlsx').iloc[:, 0].to_list()
df_incompleto = [str(x) for x in df_incompleto]
df_completo = pd.read_excel('completo2.xlsx').iloc[:, 0].to_list()
df_completo = [str(x) for x in df_completo]



faltantes = []

for completo in df_completo:
    if str(completo) in df_incompleto:
        continue
    else:
        faltantes.append((completo, 'Hace falta'))

print('La lista de incompletos')
for elemento in faltantes:
    print(elemento)


print(len(faltantes))

infaltantes = []

for completo in df_incompleto:
    if str(completo) in df_completo:
        continue
    else:
        infaltantes.append((completo, 'Hace falta'))

print('La lista de incompletos')
for elemento in infaltantes:
    print(elemento)







