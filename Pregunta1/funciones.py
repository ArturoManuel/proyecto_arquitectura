import numpy as np
import pprint
from datetime import date, datetime
import requests

def get_csv():
    csv_url = 'https://jobenas-misc-bucket.s3.amazonaws.com/household_power_consumption.csv'
    req = requests.get(csv_url)
    url_content = req.content
    csv_name = csv_url.split('/')[3]
    csv_file = open(csv_name, 'wb')
    csv_file.write(url_content)
    csv_file.close()
 
def get_cols():
    #Creamos el objeto para el archivo
    archivo = open('household_power_consumption.csv','r')
    cabecera = archivo.readline()
    archivo.close()
    return cabecera

def get_day(fecha_entrada):

    #Creamos el objeto para el archivo
    archivo = open('household_power_consumption.csv','r')
    archivo.readline()

    puntos_fecha = []
    lista_hora = []

    # Iteramos en todo el archivo
    c=0
    for linea in archivo:
        # Leemos linea por linea
        lista_linea = linea.split(',')

        # Leemos la fecha y los demas datos
        fecha, hora = lista_linea[0].split(' ')# fecha y hora
        datos = lista_linea[1:]# datos de voltaje y potencia
        # Convertimos la fecha a formato AAAA/MM/DD
        fecha = fecha.replace('-','/',2)
        if(fecha == fecha_entrada):
            puntos_fecha.append(datos)
            lista_hora.append(hora)

    archivo.close()
    return np.array(puntos_fecha).astype(float), lista_hora
def get_power(fecha_entrada):
    # Obtenemos los datos
    datos, _ = get_day(fecha_entrada)
    # Obtenemos la potencia reactiva y activa de todos los puntos
    p_activa = datos[:,0] # P 

    return round(np.sum(p_activa),3)
def get_mean(fecha_entrada):
    
     # Obtenemos los datos
    datos, _ = get_day(fecha_entrada)
    # Obtenemos la potencia reactiva y activa de todos los puntos
    p_activa = datos[:,0] # P
    # Retornamos el promedio
    return round(np.mean(p_activa),3)

def get_max(fecha_entrada):

    # Obtenemos los datos
    datos, horas = get_day(fecha_entrada)
    # Obtenemos la potencia activa de todos los puntos
    p_activa = datos[:,0] # P
    # Armamos el diccionario solicitado y lo devolvemos
    return {"potencia": np.amax(p_activa), "hora": horas[np.argmax(p_activa)]}

def get_min(fecha_entrada):

    # Obtenemos los datos
    datos, horas = get_day(fecha_entrada)
    # Obtenemos la potencia reactiva y activa de todos los puntos
    p_activa = datos[:,0] # P
    # Armamos el diccionario solicitado y lo devolvemos
    return {"potencia": np.amin(p_activa), "hora": horas[np.argmin(p_activa)]}

def gen_day_dict(fecha_entrada, fecha_fin):
    diccionario={}
    lista_fechas=[]
    # La funcion extract_dates extrae las fechas comprendidas entre fecha_entrada y fecha_fin
    lista_fechas=extract_fechas(fecha_entrada, fecha_fin)
    # Parte secuencialmente
    for fecha in lista_fechas:
        diccionario[fecha]=get_day(fecha)[0]

    return diccionario

#Obtenemos las fechas entre periodos
def extract_fechas(fecha_inicio, fecha_fin):
    lista_fechas=[]
    archivo = open('household_power_consumption.csv','r')
    archivo.readline()
    fecha_inicio_dt = datetime.strptime(fecha_inicio,'%Y/%m/%d').date()
    fecha_fin_dt = datetime.strptime(fecha_fin,'%Y/%m/%d').date()
    # Iteramos en todo el archivo
    for linea in archivo:
        # Leemos linea por linea
        lista_linea = linea.split(',')

        # Leemos la fecha y los demas datos
        fecha, _ = lista_linea[0].split(' ')# fecha y hora
        fecha_dt = datetime.strptime(fecha,'%Y-%m-%d').date() # Formato datetime (para comparar)
        fecha = fecha.replace('-','/',2) # Convertimos la fecha a formato AAAA/MM/DD
        # Comparamos las fechas y agregamos al diccionario
        if fecha_dt >= fecha_inicio_dt and fecha_dt <= fecha_fin_dt and not(fecha in lista_fechas):
            lista_fechas.append(fecha)
        if fecha_dt > fecha_fin_dt:
            break
    archivo.close()
    return lista_fechas

def extract_datos(fecha):
    resultado={}
    # Se obtiene las potencias
    potMax=get_max(fecha)["potencia"]
    potMin=get_min(fecha)["potencia"]
    potMean=get_mean(fecha)
    potTotal=get_power(fecha)
    resultado =dict(potencia_Maxima= potMax,potencia_Minima=potMin,potencia_Promedio=potMean,Total=potTotal)
    return resultado

#Obtenemos el archivo csv
# get_csv()

# Obtenemos los nombres de las columnas
#cabecera = get_cols()
#print(cabecera)

#fecha = '2006/12/16'
# Obtenemos los datos de la fecha introducida
#datos = get_day(fecha)
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(datos)
#fecha = '2007/12/16'
# Obtenemos el promedio de potencia de la fecha introducida
#promedio = get_mean(fecha)
#print(f'Promedio de potencia global del dia {fecha}: {promedio}')

#fecha = '2007/12/16'
# Obtenemos la potencia maxima de la fecha introducida
#potencia_max = get_max(fecha)
#print(f'Potencia maxima global del dia {fecha}: {potencia_max}')

#fecha = '2007/12/16'
# Obtenemos la potencia maxima de la fecha introducida
#potencia_min = get_min(fecha)
#print(f'Potencia minima global del dia {fecha}: {potencia_min}')

# Creamos el diccionario con fecha inicio y fecha fin
#diccionario = gen_day_dict('2008/08/21','2008/08/22')
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(diccionario)

# Ejecutamos extract_fechas para obtener las fechas entre los dos parametros de entrada
#lista_fechas=[]
#lista_fechas=extract_fechas('2008/08/21','2008/09/02')
#print(lista_fechas)

# Ejecutamos extract_datos
#diccionario=extract_datos('2008/08/21')
#print(diccionario)