import random
from multiprocessing import Process, Array
from multiprocessing import BoundedSemaphore, Semaphore

NPROD = random.randint(1,15)
NCONS = random.randint(1,15)
N = random.randint(1,15)

#La funciÃ³n minimo_buffer se encarga de calcular el mÃ­nimo del buffer. 
def minimo_buffer(lista):
    lista_auxiliar = [0]*len(lista)
    max_lista = max(lista)
    for i in range(len(lista)):
        if lista[i] == -1: # Se comprueba si el elemento de la lista es -1
            lista_auxiliar[i] = max_lista + 1
        else:
            lista_auxiliar[i] = lista[i] 
    minimo_lista = lista_auxiliar[0]
    posicion = 0
    for i in range(1, len(lista_auxiliar)):
        if lista_auxiliar[i] < minimo_lista and lista_auxiliar[i] != -1:
            minimo_lista = lista_auxiliar[i]
            posicion = i
    return minimo_lista, posicion

    

def productor(lista, buffer, posicion):
     v = 0
     for k in range(N):
         v += random.randint(1,7)
         lista[2*posicion].acquire()
         buffer[posicion] = v
         lista[2*posicion+1].release()
     v = -1
     lista[2*posicion].acquire()
     buffer[posicion] = v
     lista[2*posicion+1].release()
     


def consumidor(lista, buffer):  
    numeros = []
    for i in range(NPROD):
        lista[2*i+1].acquire()
    while [-1]*NPROD != list(buffer):
        v, posicion = minimo_buffer(buffer)
        numeros.append(v)
        lista[2*posicion].release()
        lista[2*posicion + 1].acquire()
    print ('Valor final de la lista:', numeros)
    
    

def main():
     buffer = Array('i', NPROD)
     lista_semaforo = []
     for i in range(NPROD):
         lista_semaforo.append(BoundedSemaphore(1))
         lista_semaforo.append(Semaphore(0))
     lista_procesos = []
     for index in range(NPROD):
         lista_procesos.append(Process(target=productor, args=(lista_semaforo, buffer, index)))
     lista_procesos.append(Process(target=consumidor, args=(lista_semaforo, buffer))) 
     for p in lista_procesos:
         p.start()
     for p in lista_procesos:
         p.join()



if __name__ == "__main__":
 main()    
           

        