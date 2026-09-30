"""
generador.py
Herramienta para provocar carga intensiva usando todos los nucleos de CPU.
"""
import time
import math
from multiprocessing import Process, cpu_count

def tarea_cpu():
    # Bucle infinito de calculo
    while True:
        _ = [math.sqrt(i) ** 2 for i in range(10000)]

def estresar_cpu(segundos=10):
    num_nucleos = cpu_count()
    print(f"\n[GENERADOR] Provocando carga ALTA en {num_nucleos} nucleos durante {segundos} segundos...")
    
    procesos = []
    for _ in range(num_nucleos):
        p = Process(target=tarea_cpu)
        p.start()
        procesos.append(p)
        
    time.sleep(segundos)
    
    for p in procesos:
        p.terminate()
        p.join()
        
    print("[GENERADOR] Carga de CPU finalizada.")

if __name__ == "__main__":
    estresar_cpu(10)