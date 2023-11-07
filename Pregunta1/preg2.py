# Para importar todas las funciones del modulo funciones
import funciones as func
from time import perf_counter
import threading
from datetime import date, datetime
import concurrent.futures
import pprint
from multiprocessing import Pool
 
def get_exec_time_a():
    start = perf_counter()
    func.get_csv()
    end = perf_counter()
    exec_time = (end-start)*1e06
    print(f"El tiempo de ejecucion para leer el archivo CSV es: {round(exec_time,3)}us")

def get_exec_time_b():
    start = perf_counter()
    func.gen_day_dict('2008/08/21','2008/08/30')
    end = perf_counter()
    exec_time = (end-start)*1e06
    print(f"El tiempo de ejecucion para obtener los dias en  el archivo CSV es: {round(exec_time,3)}us")

def gen_day_dict_threaded(fecha_inicio, fecha_fin):
    
    diccionario={}
    lista_fechas=[]
    lista_fechas=func.extract_fechas(fecha_inicio, fecha_fin)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(func.get_day, lista_fechas)
        for i, result in enumerate(results):
            diccionario[lista_fechas[i]] = result[0]
    
    return diccionario

def gen_day_dict_multi(fecha_inicio, fecha_fin,numproc):

    diccionario={}
    lista_fechas=[]
    lista_fechas=func.extract_fechas(fecha_inicio, fecha_fin)

    lista_fechas = list(lista_fechas)

    # Parte de Multiprocessing
    p = Pool(numproc)
    resultados = p.map(func.get_day, lista_fechas)
    p.close()
    p.join()

    for i, resultado in enumerate(resultados):
        diccionario[lista_fechas[i]] = resultado[0]

    return diccionario

def  calc_speedup_e():
    fecha_inicio='2008/08/21'
    fecha_fin='2008/09/01'
    start = perf_counter()
    diccionario = func.gen_day_dict(fecha_inicio, fecha_fin)
    end = perf_counter()
    non_threaded_time = end-start

    start = perf_counter()
    diccionario = gen_day_dict_threaded(fecha_inicio, fecha_fin)
    end = perf_counter()
    threaded_time = end-start

    numproc=input("Ingrese el numero de procesos: ")
    numproc=int(numproc)
    start = perf_counter()
    diccionario = gen_day_dict_multi(fecha_inicio, fecha_fin,numproc)
    end = perf_counter()
    multi_time = end-start
    

    spu_nth_th=round(non_threaded_time/threaded_time ,3)
    spu_nth_mtp=round(non_threaded_time/multi_time,3)

    print(f"El speed_up con threading: {spu_nth_th}")
    print(f"El speed_up con multiprocessing: {spu_nth_mtp}")

    if spu_nth_mtp > spu_nth_th:
        print("El mejor desempeño la tuvo el multiprocessing")
    else:
        print("El mejor desempeño la tuvo multihilos")

def calc_stats(fecha_inicio, fecha_fin):
    diccionario={}
    list_date=[]
    list_date=func.extract_fechas(fecha_inicio, fecha_fin)
    for fecha in list_date:
        diccionario[fecha]=func.extract_datos(fecha)
    return diccionario

def calc_stats_conc(fecha_inicio, fecha_fin,numproc):
    diccionario={}
    lista_fechas=[]
    lista_fechas=func.extract_fechas(fecha_inicio, fecha_fin)
    lista_fechas = list(lista_fechas)
    # Esta parte usa multiprocessing para paralelizar extract_datos
    p = Pool(numproc)
    resultados = p.map(func.extract_datos, lista_fechas)
    p.close()
    p.join()

    for i, resultado in enumerate(resultados):
        diccionario[lista_fechas[i]] = resultado
    #Esta parte comentada usa threads para paralelizar extract_datos
    """with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(func.extract_datos, lista_fechas)
        for i, result in enumerate(results):
            diccionario[lista_fechas[i]] = result"""
    return diccionario

def  calc_speedup_h():
    start = perf_counter()
    diccionario = calc_stats('2008/08/21','2008/08/28')
    end = perf_counter()
    non_threaded_time = end-start
    numproc=input("Ingrese el numero de procesos: ")
    numproc=int(numproc)    
    start = perf_counter()
    diccionario = calc_stats_conc('2008/08/21','2008/08/28',numproc)
    end = perf_counter()
    threaded_time = end-start

    print(f"El speed_up con multiprocess para calc_stats: {round(non_threaded_time/threaded_time ,3)}")

def verif_gen_day_dict():
    diccionario={}
    diccionario_th={}
    diccionario_mp={}
    lista_fechas=[]
    numproc=4
    fecha_entrada='2008/08/21'
    fecha_fin='2008/08/30'
    diccionario=func.gen_day_dict(fecha_entrada,fecha_fin)
    diccionario_th=gen_day_dict_threaded(fecha_entrada,fecha_fin)
    diccionario_mp=gen_day_dict_multi(fecha_entrada,fecha_fin,numproc)
    lista_fechas=func.extract_fechas(fecha_entrada, fecha_fin)
    #print(diccionario)
    #print(diccionario_th)
    #print(diccionario_mp)
    for fecha in lista_fechas:
        lista_non_th=list(diccionario[fecha])
        lista_th=list(diccionario_th[fecha])
        lista_mp=list(diccionario_mp[fecha])
        for i in range(len(lista_non_th)):
            if set(lista_non_th[i])==set(lista_th[i])==set(lista_mp[i]):
                val=1
            else:
                val=0
                break
        if val==0:
            break
    if val==1:
        print("Los valores de la funcion gen_day_dict ejecutada secuencial y concurrente son iguales")
    else:
        print("Los valores de la funcion gen_day_dict ejecutada secuencial y concurrente son diferentes")
    
def verif_calc_stats():
    fecha_entrada='2008/08/21'
    fecha_fin='2008/08/25'
    lista_fechas=[]
    diccionario={}
    diccionario_conc={}
    numproc=4
    diccionario=calc_stats(fecha_entrada,fecha_fin)
    diccionario_conc=calc_stats_conc(fecha_entrada,fecha_fin,numproc)
    lista_fechas=func.extract_fechas(fecha_entrada, fecha_fin)
    #print(diccionario)
    #print(diccionario_conc)
    for fecha in lista_fechas:
        if diccionario[fecha]==diccionario_conc[fecha]:
            val=1
        else:
            val=0
            break
    if val==1:
        print("Los valores de la funcion calc_stats ejecutada secuencial y concurrente son iguales")
    else:
        print("Los valores de la funcion calc_stats ejecutada secuencial y concurrente son diferentes")
if __name__ == "__main__":
    #get_exec_time_a()
    #get_exec_time_b()}

    #diccionario=gen_day_dict_threaded('2008/08/21','2008/08/22')
    #print(diccionario)

    #numproc=input("Ingrese el numero de procesos: ")
    #numproc=int(numproc)
    #diccionario=gen_day_dict_multi('2008/08/21','2008/08/22',numproc)
    #print(diccionario)

    verif_gen_day_dict()

    #calc_speedup_e()

    #diccionario={}
    
    #diccionario=calc_stats('2008/08/21','2008/08/30')
    #print(diccionario)
    
    #numproc=input("Ingrese el numero de procesos: ")
    #numproc=int(numproc)
    
    #diccionario=calc_stats_conc('2008/08/21','2008/08/30',numproc)
    #print(diccionario)
    
    #verif_calc_stats()

    #calc_speedup_h()
    